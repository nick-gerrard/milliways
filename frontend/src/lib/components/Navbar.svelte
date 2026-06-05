<script lang="ts">
  import { page } from "$app/state";
  import { PUBLIC_API_URL } from "$env/static/public";
  import type { User } from "$lib/types";
  import Logo from "$lib/components/Logo.svelte";
  import Button from "$lib/components/Button.svelte";

  interface NavLink {
    label: string;
    href: string;
  }

  interface Props {
    brand?: string;
  }

  let { brand = "Milliways" }: Props = $props();
  let menuOpen = $state(false);
  let dropdownOpen = $state(false);
  let user = $state<User | null>(null);

  const links: NavLink[] = [
    { label: "Home", href: "/" },
    { label: "Recipes", href: "/recipes" },
    { label: "Shop", href: "/shop" },
    { label: "About", href: "/about" },
  ];

  function toggleMenu() {
    menuOpen = !menuOpen;
  }

  function toggleDropdown() {
    dropdownOpen = !dropdownOpen;
  }

  function initials(name: string) {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  }

  async function fetchUser() {
    const res = await fetch(`${PUBLIC_API_URL}/auth/me`, { credentials: "include" });
    user = res.ok ? await res.json() : null;
  }

  fetchUser();
</script>

<nav
  class="sticky top-0 z-50 flex h-16 items-center justify-between gap-4 border-b border-white/20 bg-white/10 backdrop-blur-md"
>
  <a href="/" class="px-8">
    <Logo size="sm" />
  </a>
  <div>
    <ul class="hidden items-center justify-center gap-8 px-8 md:flex">
      {#each links as link}
        <li
          class={page.url.pathname === link.href
            ? "rounded-full border border-white/20 p-2 font-bold text-fuchsia-400 shadow-lg backdrop-blur-lg"
            : "text-white"}
        >
          <a href={link.href}>{link.label}</a>
        </li>
      {/each}
    </ul>
  </div>
  <div class="relative px-8">
    {#if user}
      <button
        onclick={toggleDropdown}
        class="flex hidden h-9 w-9 items-center justify-center rounded-full bg-violet-600 text-sm font-bold text-white transition-colors hover:bg-violet-500 md:block"
      >
        {initials(user.name)}
      </button>
      {#if dropdownOpen}
        <div
          class="absolute top-12 right-4 z-50 min-w-40 rounded-lg border border-white/20 bg-slate-900/95 py-1 shadow-xl backdrop-blur-md"
        >
          <p class="px-4 py-2 text-sm text-white/60">{user.name}</p>
          <hr class="border-white/10" />
          <a
            href="{PUBLIC_API_URL}/auth/logout"
            class="flex items-center gap-2 px-4 py-2 text-sm text-red-400 transition-colors hover:bg-white/10 hover:text-red-300"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-4"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15"
              />
            </svg>
            Sign out
          </a>
        </div>
      {/if}
    {:else}
      <Button href="{PUBLIC_API_URL}/auth/login" variant="primary" class="hidden md:block">Sign in with Google</Button>
    {/if}
  </div>
  <button class="px-8 text-2xl text-white md:hidden" onclick={toggleMenu} aria-label="hamburger">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
    </svg>
  </button>
</nav>

{#if dropdownOpen}
  <button class="fixed inset-0 z-40 cursor-default" onclick={toggleDropdown} aria-label="Close dropdown"></button>
{/if}
{#if menuOpen}
  <button class="fixed inset-0 z-40 cursor-default bg-black/50 md:hidden" onclick={toggleMenu} aria-label="Close menu"
  ></button>
{/if}
<div
  class="fixed right-0 bottom-0 left-0 z-50 border-t border-white/20 bg-white/10 backdrop-blur-md transition-transform duration-300 md:hidden {menuOpen
    ? 'translate-y-0'
    : 'translate-y-full'}"
>
  <ul class="flex flex-col items-center gap-6 py-8">
    {#each links as link}
      <li class={page.url.pathname === link.href ? "font-bold text-fuchsia-400" : "text-white"}>
        <a href={link.href} onclick={toggleMenu}>{link.label}</a>
      </li>
    {/each}
    {#if user}
      <li>
        <a
          href="{PUBLIC_API_URL}/auth/logout"
          class="flex items-center gap-2 px-4 py-2 text-sm text-red-400 transition-colors hover:bg-white/10 hover:text-red-300"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="size-4"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15"
            />
          </svg>
          Sign out
        </a>
      </li>
    {:else}
      <Button href="{PUBLIC_API_URL}/auth/login" variant="primary">Sign in with Google</Button>
    {/if}
  </ul>
</div>
