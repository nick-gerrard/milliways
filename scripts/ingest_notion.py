#!/usr/bin/env python3
"""
Notion recipe ingestion script — two phases:

  Phase 1 (download): Walks the Notion recipe DB, finds PDF file attachments
                      on each page, and saves them to data/pdfs/.
                      Non-PDF attachments and pages with no files are logged
                      to data/skipped.jsonl.

  Phase 2 (parse):    For each PDF in data/pdfs/, extracts text with
                      pdfplumber, sends it to an Ollama model, and writes
                      the resulting recipe JSON to data/json/.

Usage:
    python scripts/ingest_notion.py --phase download
    python scripts/ingest_notion.py --phase parse

Required env vars:
    NOTION_TOKEN          — Notion integration secret
    NOTION_DATABASE_ID    — ID of your recipe database

Optional env vars:
    OLLAMA_MODEL          — model name (default: gemma3)
    OLLAMA_HOST           — Ollama base URL (default: http://localhost:11434)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "backend" / ".env")

import httpx
import pdfplumber
import ollama

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DB_ID") or os.environ.get("NOTION_DATABASE_ID")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

DATA_DIR = Path(__file__).parent.parent / "data"
PDF_DIR = DATA_DIR / "pdfs"
JSON_DIR = DATA_DIR / "json"
SKIPPED_LOG = DATA_DIR / "skipped.jsonl"

# Schema sent to the model — mirrors the Recipe/RecipeIngredient/RecipeStep models
RECIPE_JSON_SCHEMA = {
    "name": "string (required)",
    "description": "string or null",
    "servings": "integer (required — estimate if not stated)",
    "prep_time_minutes": "integer or null",
    "cook_time_minutes": "integer or null",
    "author": "string or null",
    "source_url": "string or null",
    "image_url": "string or null",
    "ingredients": [
        {
            "name": "string",
            "quantity": "number (convert fractions: 1/2 = 0.5, 1/4 = 0.25)",
            "unit": "string (e.g. cup, tbsp, g, oz, whole)",
            "notes": "string or null",
        }
    ],
    "steps": [
        {
            "order": "integer starting at 1",
            "instruction": "string",
        }
    ],
    "tags": ["string (cuisine type, meal type, dietary info, etc.)"],
}

PARSE_PROMPT = """\
You are a recipe parser. Extract all recipe information from the text below.
Return ONLY a single valid JSON object — no markdown code fences, no explanation, no extra text.
Match this schema exactly:

{schema}

Recipe text:
{text}"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def slugify(name: str) -> str:
    slug = name.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-")[:100]


def log_skip(title: str, reason: str, extra: dict | None = None) -> None:
    entry = {"title": title, "reason": reason, **(extra or {})}
    with SKIPPED_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"  SKIP [{reason}]: {title}")


def get_page_title(page: dict) -> str:
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(p.get("plain_text", "") for p in prop.get("title", []))
    return page["id"]


NOTION_API = "https://api.notion.com/v1"
NOTION_HEADERS = {
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def notion_get(path: str, token: str) -> dict:
    url = f"{NOTION_API}/{path}"
    r = httpx.get(url, headers={**NOTION_HEADERS, "Authorization": f"Bearer {token}"}, timeout=30)
    r.raise_for_status()
    return r.json()


def notion_post(path: str, token: str, body: dict) -> dict:
    url = f"{NOTION_API}/{path}"
    r = httpx.post(url, headers={**NOTION_HEADERS, "Authorization": f"Bearer {token}"}, json=body, timeout=30)
    r.raise_for_status()
    return r.json()


def get_all_blocks(token: str, block_id: str) -> list[dict]:
    """Fetch all blocks for a page/block, walking children recursively."""
    blocks: list[dict] = []
    cursor = None
    while True:
        params = f"?start_cursor={cursor}" if cursor else ""
        response = notion_get(f"blocks/{block_id}/children{params}", token)
        for block in response["results"]:
            blocks.append(block)
            if block.get("has_children"):
                blocks.extend(get_all_blocks(token, block["id"]))
        if not response.get("has_more"):
            break
        cursor = response["next_cursor"]
    return blocks


def find_pdf_blocks(blocks: list[dict]) -> list[dict]:
    """Return blocks that are PDFs or .pdf file attachments."""
    result = []
    for block in blocks:
        btype = block.get("type")
        if btype == "pdf":
            result.append(block)
        elif btype == "file":
            name = block.get("file", {}).get("name", "")
            if name.lower().endswith(".pdf"):
                result.append(block)
    return result


def find_non_pdf_files(blocks: list[dict]) -> list[dict]:
    """Return non-PDF file/image blocks (used to explain why a page was skipped)."""
    result = []
    for block in blocks:
        btype = block.get("type")
        if btype == "image":
            result.append(block)
        elif btype == "file":
            name = block.get("file", {}).get("name", "")
            if not name.lower().endswith(".pdf"):
                result.append(block)
    return result


def get_file_url(block: dict) -> str | None:
    btype = block.get("type")
    block_data = block.get(btype, {})
    for key in ("file", "external"):
        info = block_data.get(key)
        if isinstance(info, dict):
            return info.get("url")
    return None


def download_file(url: str, dest: Path) -> bool:
    try:
        with httpx.stream("GET", url, follow_redirects=True, timeout=60) as r:
            r.raise_for_status()
            with dest.open("wb") as f:
                for chunk in r.iter_bytes(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"    Download error: {e}")
        return False


def extract_json(raw: str) -> dict | None:
    """Pull a JSON object out of a model response, tolerating markdown fences."""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text.strip())
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Last-ditch: find first {...} block in the response
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


# ---------------------------------------------------------------------------
# Phase 1: Download
# ---------------------------------------------------------------------------


def download_phase() -> None:
    if not NOTION_TOKEN:
        sys.exit("Error: NOTION_TOKEN env var is not set")
    if not NOTION_DATABASE_ID:
        sys.exit("Error: NOTION_DATABASE_ID env var is not set")

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SKIPPED_LOG.write_text("")  # reset skip log

    # Paginate through the entire database
    pages: list[dict] = []
    cursor = None
    while True:
        body: dict = {}
        if cursor:
            body["start_cursor"] = cursor
        response = notion_post(f"databases/{NOTION_DATABASE_ID}/query", NOTION_TOKEN, body)
        pages.extend(response["results"])
        if not response.get("has_more"):
            break
        cursor = response["next_cursor"]

    print(f"Found {len(pages)} pages in Notion database\n")

    # Look up the "Recipe" files property ID from the database schema
    db = notion_get(f"databases/{NOTION_DATABASE_ID}", NOTION_TOKEN)
    recipe_prop_id = None
    for name, prop in db.get("properties", {}).items():
        if name.lower() == "recipe" and prop["type"] == "files":
            recipe_prop_id = prop["id"]
            break
    if not recipe_prop_id:
        sys.exit("Could not find a 'Recipe' files property in the database schema")
    print(f"Recipe property ID: {recipe_prop_id}\n")

    downloaded = skipped = 0

    for page in pages:
        title = get_page_title(page)
        print(f"Processing: {title}")

        # Fetch the Recipe property directly — databases/query returns empty files arrays
        try:
            prop_data = notion_get(f"pages/{page['id']}/properties/{recipe_prop_id}", NOTION_TOKEN)
            files = prop_data.get("files", [])
        except Exception as e:
            log_skip(title, "api_error", {"error": str(e)})
            skipped += 1
            continue

        pdf_files = [f for f in files if f.get("name", "").lower().endswith(".pdf") or f.get("type") == "file"]

        if not pdf_files:
            non_pdf = [f for f in files if f not in pdf_files]
            reason = "non_pdf_files_only" if non_pdf else "no_attachments"
            log_skip(title, reason, {"non_pdf_count": len(non_pdf)})
            skipped += 1
            continue

        slug = slugify(title)

        for i, f in enumerate(pdf_files):
            # Notion internal files use f["file"]["url"]; external use f["external"]["url"]
            if f.get("type") == "file":
                url = f["file"]["url"]
            elif f.get("type") == "external":
                url = f["external"]["url"]
            else:
                log_skip(title, "no_url", {"file": f.get("name")})
                skipped += 1
                continue

            suffix = f"_{i}" if i > 0 else ""
            dest = PDF_DIR / f"{slug}{suffix}.pdf"

            if dest.exists():
                print(f"  Already exists: {dest.name}")
                downloaded += 1
                continue

            print(f"  Downloading → {dest.name}")
            if download_file(url, dest):
                downloaded += 1
            else:
                log_skip(title, "download_failed", {"url": url[:120]})
                skipped += 1

    print(f"\nFinished — downloaded: {downloaded}, skipped: {skipped}")
    print(f"PDFs:     {PDF_DIR}")
    print(f"Skip log: {SKIPPED_LOG}")


# ---------------------------------------------------------------------------
# Phase 2: Parse
# ---------------------------------------------------------------------------


def parse_phase(limit: int | None = None) -> None:
    if not PDF_DIR.exists() or not any(PDF_DIR.glob("*.pdf")):
        sys.exit(f"No PDFs found in {PDF_DIR}. Run --phase download first.")

    JSON_DIR.mkdir(parents=True, exist_ok=True)

    # Configure Ollama client host if non-default
    client = ollama.Client(host=OLLAMA_HOST)

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if limit:
        pdfs = pdfs[:limit]
    total = len(pdfs)
    print(f"Found {total} PDF(s) to parse with model '{OLLAMA_MODEL}' at {OLLAMA_HOST}\n")

    parsed = failed = skipped_existing = 0

    for i, pdf_path in enumerate(pdfs, start=1):
        out_path = JSON_DIR / pdf_path.with_suffix(".json").name

        if out_path.exists():
            print(f"[{i}/{total}] Skipping (already parsed): {pdf_path.name}")
            skipped_existing += 1
            continue

        print(f"[{i}/{total}] Parsing: {pdf_path.name}")

        # --- Extract text ---
        try:
            pages_text: list[str] = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
        except Exception as e:
            print(f"  ERROR reading PDF: {e}")
            log_skip(pdf_path.stem, "pdf_read_error", {"file": pdf_path.name, "error": str(e)})
            failed += 1
            continue

        if not pages_text:
            print("  ERROR: no text extracted — likely a scanned/image-only PDF")
            log_skip(pdf_path.stem, "no_text_extracted", {"file": pdf_path.name})
            failed += 1
            continue

        print(f"  Extracted {len(pages_text)} page(s) of text, sending to Ollama...")
        full_text = "\n\n".join(pages_text)

        # --- Send to Ollama ---
        prompt = PARSE_PROMPT.format(
            schema=json.dumps(RECIPE_JSON_SCHEMA, indent=2),
            text=full_text[:10_000],  # stay within typical context limits
        )

        try:
            response = client.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.message.content
        except Exception as e:
            print(f"  ERROR from Ollama: {e}")
            log_skip(pdf_path.stem, "ollama_error", {"error": str(e)})
            failed += 1
            continue

        # --- Parse JSON ---
        recipe = extract_json(raw)

        if recipe is None:
            print("  ERROR: could not parse JSON from model response — saving raw output for inspection")
            raw_path = JSON_DIR / f"{pdf_path.stem}.raw.txt"
            raw_path.write_text(raw)
            log_skip(pdf_path.stem, "json_parse_failed", {"raw_saved": raw_path.name})
            failed += 1
            continue

        recipe["_source"] = {"pdf": pdf_path.name, "model": OLLAMA_MODEL}
        out_path.write_text(json.dumps(recipe, indent=2, ensure_ascii=False))
        print(f"  Done → {out_path.name}  ({parsed + 1}/{total - skipped_existing} complete)")
        parsed += 1

    print(f"\n{'='*50}")
    print(f"Finished: {parsed} parsed, {failed} failed, {skipped_existing} already done")
    if failed:
        print(f"Failures logged: {SKIPPED_LOG}")
    print(f"JSON output: {JSON_DIR}")


# ---------------------------------------------------------------------------
# Phase 3: Ingest JSON into the database
# ---------------------------------------------------------------------------


def parse_quantity(value) -> float:
    """Convert a quantity value to float, handling ranges and fractions."""
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    # Take the first number from a range like "1.5 to 2" or "1-2"
    match = re.match(r"[\d]*\.?[\d]+", s)
    if match:
        return float(match.group())
    return 0.0


def ingest_phase(force: bool = False) -> None:
    if not JSON_DIR.exists() or not any(JSON_DIR.glob("*.json")):
        sys.exit(f"No JSON files found in {JSON_DIR}. Run --phase parse first.")

    # Add backend to path so we can import app models directly
    backend_dir = Path(__file__).parent.parent / "backend"
    sys.path.insert(0, str(backend_dir))

    from sqlmodel import Session, select, create_engine
    from app.models import Recipe, Ingredient, RecipeIngredient, RecipeStep, Tag, RecipeTag

    db_url = os.environ.get("DATABASE_URL", f"sqlite:///{backend_dir}/milliways.db")
    engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})

    json_files = sorted(JSON_DIR.glob("*.json"))
    # Exclude raw debug output files saved by the parse phase
    json_files = [f for f in json_files if not f.stem.endswith(".raw")]
    total = len(json_files)
    print(f"Found {total} JSON file(s) to ingest into {db_url}\n")

    inserted = skipped = failed = 0

    with Session(engine) as session:
        for i, json_path in enumerate(json_files, start=1):
            try:
                data = json.loads(json_path.read_text())
            except Exception as e:
                print(f"[{i}/{total}] ERROR reading {json_path.name}: {e}")
                failed += 1
                continue

            name = data.get("name", "").strip()
            if not name:
                print(f"[{i}/{total}] SKIP (no name): {json_path.name}")
                skipped += 1
                continue

            # Check for duplicate
            existing = session.exec(select(Recipe).where(Recipe.name == name)).first()
            if existing and not force:
                print(f"[{i}/{total}] SKIP (already exists): {name}")
                skipped += 1
                continue
            if existing and force:
                # Delete old related records before replacing
                session.exec(  # type: ignore
                    select(RecipeIngredient).where(RecipeIngredient.recipe_id == existing.id)
                )
                for ri in session.exec(select(RecipeIngredient).where(RecipeIngredient.recipe_id == existing.id)).all():
                    session.delete(ri)
                for rs in session.exec(select(RecipeStep).where(RecipeStep.recipe_id == existing.id)).all():
                    session.delete(rs)
                for rt in session.exec(select(RecipeTag).where(RecipeTag.recipe_id == existing.id)).all():
                    session.delete(rt)
                session.delete(existing)
                session.flush()

            print(f"[{i}/{total}] Inserting: {name}")

            # --- Recipe ---
            recipe = Recipe(
                name=name,
                description=data.get("description"),
                servings=data.get("servings") or 1,
                prep_time_minutes=data.get("prep_time_minutes"),
                cook_time_minutes=data.get("cook_time_minutes"),
                source_url=data.get("source_url"),
                author=data.get("author"),
                image_url=data.get("image_url"),
                is_public=False,
            )
            session.add(recipe)
            session.flush()  # get recipe.id before adding related records

            # --- Ingredients ---
            for ing_data in data.get("ingredients", []):
                ing_name = ing_data.get("name", "").strip()
                if not ing_name:
                    continue
                ingredient = session.exec(
                    select(Ingredient).where(Ingredient.name == ing_name)
                ).first()
                if not ingredient:
                    ingredient = Ingredient(name=ing_name)
                    session.add(ingredient)
                    session.flush()

                session.add(RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=parse_quantity(ing_data.get("quantity") or 0),
                    unit=ing_data.get("unit") or "",
                    notes=ing_data.get("notes"),
                ))

            # --- Steps ---
            for step_data in data.get("steps", []):
                instruction = step_data.get("instruction", "").strip()
                if not instruction:
                    continue
                session.add(RecipeStep(
                    recipe_id=recipe.id,
                    order=step_data.get("order", 0),
                    instruction=instruction,
                ))

            # --- Tags ---
            for tag_name in data.get("tags", []):
                tag_name = tag_name.strip()
                if not tag_name:
                    continue
                tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    session.add(tag)
                    session.flush()
                session.add(RecipeTag(recipe_id=recipe.id, tag_id=tag.id))

            session.commit()
            inserted += 1
            print(f"  Done ({inserted} inserted so far)")

    print(f"\n{'='*50}")
    print(f"Finished: {inserted} inserted, {skipped} skipped, {failed} failed")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest Notion recipes into structured JSON via Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--phase",
        required=True,
        choices=["download", "parse", "ingest"],
        help="download: fetch PDFs from Notion  |  parse: convert PDFs to JSON  |  ingest: load JSON into the DB",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="(parse only) stop after processing N PDFs",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="(ingest only) overwrite recipes that already exist in the DB",
    )
    args = parser.parse_args()

    if args.phase == "download":
        download_phase()
    elif args.phase == "parse":
        parse_phase(limit=args.limit)
    else:
        ingest_phase(force=args.force)


if __name__ == "__main__":
    main()
