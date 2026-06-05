<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { PUBLIC_API_URL } from "$env/static/public";
  import GlassCard from "$lib/components/GlassCard.svelte";
  import Button from "$lib/components/Button.svelte";

  type IngredientDraft = { ingredient_name: string; quantity: number; unit: string; notes: string };

  let name = $state("");
  let description = $state("");
  let servings = $state(1);
  let prep_time_minutes = $state<number | undefined>(undefined);
  let cook_time_minutes = $state<number | undefined>(undefined);
  let source_url = $state("");
  let author = $state("");
  let is_public = $state(false);

  let ingredients = $state<IngredientDraft[]>([]);
  let newIngredient = $state<IngredientDraft>({ ingredient_name: "", quantity: 1, unit: "", notes: "" });

  let steps = $state<string[]>([]);
  let newStep = $state("");

  let tags = $state<string[]>([]);
  let newTag = $state("");

  let submitted = $state(false);
  let saving = $state(false);
  let saveError = $state("");
  let nameError = $derived(submitted && !name.trim());
  let servingsError = $derived(submitted && (!servings || servings < 1));

  let allIngredients = $state<string[]>([]);
  let allTags = $state<string[]>([]);
  let showIngredientSuggestions = $state(false);
  let showTagSuggestions = $state(false);

  let ingredientSuggestions = $derived(
    newIngredient.ingredient_name.length > 0
      ? allIngredients
          .filter(n => n.includes(newIngredient.ingredient_name.toLowerCase().trim()))
          .slice(0, 5)
      : []
  );

  let tagSuggestions = $derived(
    newTag.length > 0
      ? allTags
          .filter(t => t.includes(newTag.toLowerCase().trim()) && !tags.includes(t))
          .slice(0, 5)
      : []
  );

  onMount(async () => {
    const [ingRes, tagRes] = await Promise.all([
      fetch(`${PUBLIC_API_URL}/recipes/ingredients/all`, { credentials: "include" }),
      fetch(`${PUBLIC_API_URL}/recipes/tags/all`, { credentials: "include" }),
    ]);
    allIngredients = (await ingRes.json()).map((i: { name: string }) => i.name);
    allTags = (await tagRes.json()).map((t: { name: string }) => t.name);
  });

  function handleIngredientKeydown(e: KeyboardEvent) {
    if (e.key === "Tab" && ingredientSuggestions.length > 0) {
      e.preventDefault();
      newIngredient.ingredient_name = ingredientSuggestions[0];
      showIngredientSuggestions = false;
    }
  }

  function handleTagKeydown(e: KeyboardEvent) {
    if (e.key === "Enter") { addTag(); return; }
    if (e.key === "Tab" && tagSuggestions.length > 0) {
      e.preventDefault();
      newTag = tagSuggestions[0];
      showTagSuggestions = false;
    }
  }

  function addIngredient() {
    if (!newIngredient.ingredient_name.trim()) return;
    ingredients = [...ingredients, { ...newIngredient }];
    newIngredient = { ingredient_name: "", quantity: 1, unit: "", notes: "" };
  }

  function removeIngredient(i: number) {
    ingredients = ingredients.filter((_, idx) => idx !== i);
  }

  function addStep() {
    if (!newStep.trim()) return;
    steps = [...steps, newStep.trim()];
    newStep = "";
  }

  function removeStep(i: number) {
    steps = steps.filter((_, idx) => idx !== i);
  }

  function addTag() {
    if (!newTag.trim() || tags.includes(newTag.trim())) return;
    tags = [...tags, newTag.trim()];
    newTag = "";
  }

  function removeTag(t: string) {
    tags = tags.filter((tag) => tag !== t);
  }

  async function handleSubmit() {
    submitted = true;
    if (!name.trim() || !servings || servings < 1) return;
    saving = true;
    saveError = "";
    const payload = {
      name,
      description: description || null,
      servings,
      prep_time_minutes: prep_time_minutes ?? null,
      cook_time_minutes: cook_time_minutes ?? null,
      source_url: source_url || null,
      author: author || null,
      is_public,
      ingredients,
      steps: steps.map((instruction, i) => ({ order: i + 1, instruction })),
      tags,
    };
    const res = await fetch(`${PUBLIC_API_URL}/recipes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      goto("/recipes");
    } else {
      saveError = "Something went wrong — please try again.";
      saving = false;
    }
  }
</script>

<div class="flex min-h-screen flex-col items-center py-12 px-4">
  <GlassCard accent class="w-full max-w-2xl">
    <h1 class="text-2xl font-bold text-white">Add Recipe</h1>

    <!-- Basic info -->
    <div class="flex flex-col gap-2">
      <label class="text-sm font-semibold text-white/70">Name *</label>
      <input bind:value={name} class="w-full rounded-lg border {nameError ? 'border-red-400/70 focus:border-red-400' : 'border-white/30 focus:border-violet-400'} bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none" placeholder="e.g. Chicken Tikka Masala" />
      {#if nameError}<p class="text-xs text-red-400 mt-1">Required</p>{/if}
    </div>

    <div class="flex flex-col gap-2">
      <label class="text-sm font-semibold text-white/70">Description</label>
      <textarea bind:value={description} class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400 resize-none" rows="2" placeholder="A short description..."></textarea>
    </div>

    <div class="grid grid-cols-3 gap-4">
      <div class="flex flex-col gap-2">
        <label class="text-sm font-semibold text-white/70">Servings *</label>
        <input bind:value={servings} type="number" min="1" class="w-full rounded-lg border {servingsError ? 'border-red-400/70 focus:border-red-400' : 'border-white/30 focus:border-violet-400'} bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none" />
        {#if servingsError}<p class="text-xs text-red-400 mt-1">Required</p>{/if}
      </div>
      <div class="flex flex-col gap-2">
        <label class="text-sm font-semibold text-white/70">Prep (mins)</label>
        <input bind:value={prep_time_minutes} type="number" min="0" class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400" />
      </div>
      <div class="flex flex-col gap-2">
        <label class="text-sm font-semibold text-white/70">Cook (mins)</label>
        <input bind:value={cook_time_minutes} type="number" min="0" class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400" />
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <label class="text-sm font-semibold text-white/70">Source URL</label>
        <input bind:value={source_url} class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400" placeholder="https://..." />
      </div>
      <div class="flex flex-col gap-2">
        <label class="text-sm font-semibold text-white/70">Author</label>
        <input bind:value={author} class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400" placeholder="e.g. Ottolenghi" />
      </div>
    </div>

    <label class="flex items-center gap-3 cursor-pointer">
      <input type="checkbox" bind:checked={is_public} class="h-4 w-4 rounded" />
      <span class="text-sm font-semibold text-white/70">Make public</span>
    </label>

    <!-- Ingredients -->
    <div class="flex flex-col gap-3">
      <label class="text-sm font-semibold text-white/70">Ingredients</label>
      <div class="grid grid-cols-[2fr_1fr_1fr_auto] gap-2 items-end">
        <div class="relative">
          <input
            bind:value={newIngredient.ingredient_name}
            onkeydown={handleIngredientKeydown}
            onfocus={() => showIngredientSuggestions = true}
            onblur={() => showIngredientSuggestions = false}
            class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400"
            placeholder="Ingredient"
          />
          {#if showIngredientSuggestions && ingredientSuggestions.length > 0}
            <ul class="absolute z-10 w-full mt-1 overflow-hidden rounded-lg border border-white/20 bg-slate-900 shadow-lg">
              {#each ingredientSuggestions as suggestion, i}
                <li>
                  <button
                    onmousedown={(e) => { e.preventDefault(); newIngredient.ingredient_name = suggestion; showIngredientSuggestions = false; }}
                    class="w-full px-3 py-2 text-left text-sm text-white hover:bg-white/10 {i === 0 ? 'bg-white/5' : ''}"
                  >{suggestion}</button>
                </li>
              {/each}
            </ul>
          {/if}
        </div>
        <input bind:value={newIngredient.quantity} type="number" min="0" step="0.1" class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400" placeholder="Qty" />
        <input bind:value={newIngredient.unit} class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400" placeholder="Unit" />
        <Button variant="secondary" onclick={addIngredient}>Add</Button>
      </div>
      {#each ingredients as ing, i}
        <div class="flex items-center justify-between rounded-lg bg-white/5 px-3 py-2 text-sm text-white">
          <span>{ing.quantity} {ing.unit} {ing.ingredient_name}{ing.notes ? ` (${ing.notes})` : ""}</span>
          <button onclick={() => removeIngredient(i)} class="text-white/40 hover:text-white ml-4">✕</button>
        </div>
      {/each}
    </div>

    <!-- Steps -->
    <div class="flex flex-col gap-3">
      <label class="text-sm font-semibold text-white/70">Steps</label>
      <div class="flex gap-2 items-end">
        <input bind:value={newStep} class="flex-1 rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400" placeholder="Describe this step..." />
        <Button variant="secondary" onclick={addStep}>Add</Button>
      </div>
      {#each steps as step, i}
        <div class="flex items-start justify-between rounded-lg bg-white/5 px-3 py-2 text-sm text-white">
          <span><span class="font-semibold text-violet-400 mr-2">{i + 1}.</span>{step}</span>
          <button onclick={() => removeStep(i)} class="text-white/40 hover:text-white ml-4 shrink-0">✕</button>
        </div>
      {/each}
    </div>

    <!-- Tags -->
    <div class="flex flex-col gap-3">
      <label class="text-sm font-semibold text-white/70">Tags</label>
      <div class="flex gap-2 items-end">
        <div class="relative flex-1">
          <input
            bind:value={newTag}
            onkeydown={handleTagKeydown}
            onfocus={() => showTagSuggestions = true}
            onblur={() => showTagSuggestions = false}
            class="w-full rounded-lg border border-white/30 bg-white/10 px-3 py-2 text-sm text-white shadow-sm placeholder:text-white/30 focus:outline-none focus:border-violet-400"
            placeholder="e.g. vegetarian"
          />
          {#if showTagSuggestions && tagSuggestions.length > 0}
            <ul class="absolute z-10 w-full mt-1 overflow-hidden rounded-lg border border-white/20 bg-slate-900 shadow-lg">
              {#each tagSuggestions as suggestion, i}
                <li>
                  <button
                    onmousedown={(e) => { e.preventDefault(); newTag = suggestion; showTagSuggestions = false; }}
                    class="w-full px-3 py-2 text-left text-sm text-white hover:bg-white/10 {i === 0 ? 'bg-white/5' : ''}"
                  >{suggestion}</button>
                </li>
              {/each}
            </ul>
          {/if}
        </div>
        <Button variant="secondary" onclick={addTag}>Add</Button>
      </div>
      {#if tags.length > 0}
        <div class="flex flex-wrap gap-2">
          {#each tags as tag}
            <span class="flex items-center gap-1 rounded-full bg-violet-600/40 px-3 py-1 text-sm text-white">
              {tag}
              <button onclick={() => removeTag(tag)} class="text-white/50 hover:text-white">✕</button>
            </span>
          {/each}
        </div>
      {/if}
    </div>

    {#if saveError}<p class="text-sm text-red-400">{saveError}</p>{/if}
    <Button variant="primary" onclick={handleSubmit} disabled={saving} class="w-full mt-2">
      {saving ? "Saving…" : "Save Recipe"}
    </Button>
  </GlassCard>
</div>

