<script lang="ts">
  import { onMount } from "svelte";
  import type { ShoppingItem } from "$lib/types";
  import Button from "$lib/components/Button.svelte";
  import GlassCard from "$lib/components/GlassCard.svelte";

  let shoppingList = $state<ShoppingItem[]>([]);
  onMount(() => {
    const stored = JSON.parse(sessionStorage.getItem("shoppingList") ?? "{}");
    shoppingList = Object.values(stored).sort((a, b) => a.name.localeCompare(b.name));
  });

  function clearShoppingList() {
    sessionStorage.clear();
    shoppingList = [];
  }
</script>

<div class="flex justify-center p-8">
  <div class="w-full max-w-lg">
    <GlassCard accent contentClass="flex flex-col gap-6">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold text-white">Shopping List</h1>
        {#if shoppingList.length > 0}
          <Button variant="warning" onclick={clearShoppingList}>Clear</Button>
        {/if}
      </div>

      {#if shoppingList.length === 0}
        <p class="text-center text-white/40 italic py-8">
          No items yet — add a recipe from the <a href="/recipes" class="text-fuchsia-400 hover:text-fuchsia-300">recipes</a> page.
        </p>
      {:else}
        <ul class="flex flex-col divide-y divide-white/10">
          {#each shoppingList as item}
            <li class="flex items-center gap-4 py-3">
              <input id={item.name} type="checkbox" class="peer h-5 w-5 shrink-0 accent-violet-500 cursor-pointer" />
              <label for={item.name} class="flex-1 cursor-pointer text-white peer-checked:line-through peer-checked:text-white/30 transition-colors">
                <span class="font-semibold">{item.quantity} {item.unit}</span>
                <span class="ml-2">{item.name}</span>
              </label>
            </li>
          {/each}
        </ul>
      {/if}
    </GlassCard>
  </div>
</div>
