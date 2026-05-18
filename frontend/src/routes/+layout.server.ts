import { redirect } from "@sveltejs/kit";
import { env } from "$env/dynamic/private";
import type { LayoutServerLoad } from "./$types";

const PUBLIC_ROUTES = ["/login"];

export const load: LayoutServerLoad = async ({ url, request }) => {
    if (PUBLIC_ROUTES.includes(url.pathname)) return {};

    const apiUrl = env.INTERNAL_API_URL ?? "http://127.0.0.1:8002";
    const cookie = request.headers.get("cookie") ?? "";
    const res = await fetch(`${apiUrl}/auth/me`, {
        headers: { cookie },
    });

    const user = res.ok ? await res.json() : null;
    if (!user) redirect(302, "/login");

    return { user };
};
