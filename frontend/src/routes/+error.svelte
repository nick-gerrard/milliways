<script lang="ts">
  import { page } from "$app/state";
  import Logo from "$lib/components/Logo.svelte";
  import GlassCard from "$lib/components/GlassCard.svelte";
  import Button from "$lib/components/Button.svelte";
</script>

<div class="flex h-[calc(100vh-4rem)] flex-col items-center justify-center gap-6">
  <GlassCard class="items-center">
    <Logo size="sm" />
    <p class="max-w-xs text-center text-sm leading-relaxed text-white/80 italic">"And so the Universe ended."</p>
    <div class="flex flex-col items-center gap-2">
      <h1 class="text-8xl font-black text-white/20">{page.status}</h1>
      <p class="text-xl font-bold text-white">{page.error?.message ?? "Something went wrong"}</p>
    </div>
    <Button class="flex justify-center border border-white/50" href="/" variant="ghost">Go home</Button>
  </GlassCard>
</div>
