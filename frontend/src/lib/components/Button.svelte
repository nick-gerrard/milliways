<script lang="ts">
  import type { Snippet } from "svelte";
  let {
    children,
    class: className = "",
    variant = "primary",
    href = undefined,
    ...restProps
  }: {
    children: Snippet;
    class?: string;
    variant?: "primary" | "secondary" | "ghost" | "warning";
    href?: string;
    [key: string]: unknown;
  } = $props();

  const variants = {
    primary: "bg-violet-600 text-white hover:bg-violet-500",
    secondary: "border border-white/20 text-white/70 hover:text-white",
    ghost: "text-white/60 hover:text-white",
    warning: "bg-red-600 text-white hover:bg-red-500",
  };

  const base = "px-4 py-2 rounded-full text-sm transition-colors";
</script>

{#if href}
  <a {href} class="{base} {variants[variant]} {className}" {...restProps}>
    {@render children()}
  </a>
{:else}
  <button class="{base} {variants[variant]} {className}" {...restProps}>
    {@render children()}
  </button>
{/if}
