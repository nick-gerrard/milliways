<script lang="ts">
    import { page } from "$app/state";
    import  Logo  from "$lib/components/Logo.svelte"
</script>

<div class="h-[calc(100vh-4rem)] flex flex-col items-center justify-center gap-6">
    <div class="flex flex-col justify-center items-center gap-8 border border-white/30 bg-white/10 rounded-lg shadow-lg p-8 backdrop-blur-md">
        <Logo size="sm"/>
        <p class="text-white/80 text-sm italic text-center max-w-xs leading-relaxed">
            "And so the Universe ended."
        </p>
    <div class="flex flex-col items-center gap-2">
        <h1 class="text-8xl font-black text-white/20">{page.status}</h1>
        <p class="text-xl font-bold text-white">{page.error?.message ?? "Something went wrong"}</p>
    </div>
    <a href="/" class="px-4 py-2 rounded-full border border-white/20 text-white/60 text-sm hover:text-white transition-colors">
        Go home
    </a>

    </div>
</div>
