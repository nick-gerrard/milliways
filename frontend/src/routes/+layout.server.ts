import { redirect } from "@sveltejs/kit";
import { env } from "$env/dynamic/private";
import type { LayoutServerLoad } from "./$types";

const PUBLIC_ROUTES = ["/login"];

export const load: LayoutServerLoad = async ({ url, cookies }) => {
    if (PUBLIC_ROUTES.includes(url.pathname)) return {};

    const apiUrl = env.INTERNAL_API_URL ?? "http://127.0.0.1:8002";
    const sessionCookie = cookies.get("session");

    if (!sessionCookie) redirect(302, "/login");

    const res = await fetch(`${apiUrl}/auth/me`, {
        headers: { cookie: `session=${sessionCookie}` },
    });

    const user = res.ok ? await res.json() : null;
    if (!user) redirect(302, "/login");

    return { user };
};
