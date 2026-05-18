import { redirect } from "@sveltejs/kit";
import { PUBLIC_API_URL } from "$env/static/public";
import type { LayoutServerLoad } from "./$types";

const PUBLIC_ROUTES = ["/login"];

export const load: LayoutServerLoad = async ({ url, request }) => {
    if (PUBLIC_ROUTES.includes(url.pathname)) return {};

    const cookie = request.headers.get("cookie") ?? "";
    const res = await fetch(`${PUBLIC_API_URL}/auth/me`, {
        headers: { cookie },
    });

    const user = res.ok ? await res.json() : null;
    if (!user) redirect(302, "/login");

    return { user };
};
