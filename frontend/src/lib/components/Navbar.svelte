<script lang="ts">
    import { page } from "$app/state";
    import { PUBLIC_API_URL } from "$env/static/public";
    import type { User } from "$lib/types";
    import Logo from "$lib/components/Logo.svelte";

    interface NavLink {
        label: string;
        href: string;
    }

    interface Props {
        brand?: string;
    }

    let { brand = "Milliways" }: Props = $props();
    let menuOpen = $state(false);
    let user = $state<User | null>(null);

    const links: NavLink[] = [
        { label: "Home", href: "/" },
        { label: "Recipes", href: "/recipes" },
        { label: "About", href: "/about" },
    ];

    function toggleMenu() {
        menuOpen = !menuOpen;
    }

    async function fetchUser() {
        const res = await fetch(`${PUBLIC_API_URL}/auth/me`, { credentials: "include" });
        user = res.ok ? await res.json() : null;
    }

    fetchUser();
</script>

<nav
    class="h-16 sticky z-50 top-0 backdrop-blur-md border-b border-white/20 bg-white/10 flex gap-4 justify-between items-center"
>
    <a href="/" class="px-8">
        <Logo size="sm" />
    </a>
    <button
        class="md:hidden px-8 text-white text-2xl"
        onclick={toggleMenu}
        aria-label="hamburger"
    >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="size-6"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
            />
        </svg>
    </button>
    <div>
    <ul class="hidden md:flex items-center justify-center gap-8 px-8">
        {#each links as link}
            <li
                class={page.url.pathname === link.href
                    ? "text-fuchsia-400 font-bold border border-white/20 rounded-full shadow-lg p-2 backdrop-blur-lg"
                    : "text-white"}
            >
                <a href={link.href}>{link.label}</a>
            </li>
        {/each}
    </ul>

    </div>
    <div>
        <ul>
        <li>
            {#if user}
                <span class="text-white/60 text-sm mr-2">{user.name}</span>
                <a href="{PUBLIC_API_URL}/auth/logout" class="px-4 py-2 rounded-full border border-white/20 text-white/70 text-sm hover:text-white transition-colors">
                    Sign out
                </a>
            {:else}
                <a href="{PUBLIC_API_URL}/auth/login" class="px-4 py-2 rounded-full bg-violet-600 text-white text-sm hover:bg-violet-500 transition-colors">
                    Sign in with Google
                </a>
            {/if}
        </li>

        </ul>
    </div>
</nav>
{#if menuOpen}
    <button
        class="fixed inset-0 bg-black/50 z-40 md:hidden cursor-default"
        onclick={toggleMenu}
        aria-label="Close menu"
    ></button>
{/if}
<div
    class="fixed bottom-0 left-0 right-0 z-50 md:hidden
           bg-white/10 backdrop-blur-md border-t border-white/20
           transition-transform duration-300
           {menuOpen ? 'translate-y-0' : 'translate-y-full'}"
>
    <ul class="flex flex-col items-center gap-6 py-8">
        {#each links as link}
            <li
                class={page.url.pathname === link.href
                    ? "text-fuchsia-400 font-bold"
                    : "text-white"}
            >
                <a href={link.href} onclick={toggleMenu}>
                    {link.label}
                </a>
            </li>
        {/each}
    </ul>
</div>
