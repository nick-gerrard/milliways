<script lang="ts">
  import type { Snippet } from "svelte";
  let {
    children,
    class: className = "",
    accent = false,
  }: { children: Snippet; class?: string; accent?: boolean } = $props();
</script>

<div class="overflow-hidden rounded-lg border border-white/30 bg-white/10 shadow-lg backdrop-blur-md {className}">
  {#if accent}
    <div class="h-2 bg-gradient-to-r from-fuchsia-400 via-green-400 to-violet-400"></div>
  {/if}
  <div class="p-8">
    {@render children()}
  </div>
</div>
