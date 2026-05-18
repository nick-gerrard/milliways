<script lang="ts">
    type Size = "sm" | "md" | "lg";
    let { size = "lg" }: { size?: Size } = $props();

    const titleClass = {
        sm: "text-xl tracking-[0.15em]",
        md: "text-3xl tracking-[0.2em]",
        lg: "text-7xl tracking-[0.2em]",
    }[size];

    const subtitleClass = {
        sm: "text-[0.5rem] tracking-[0.2em]",
        md: "text-xs tracking-[0.25em]",
        lg: "text-base tracking-[0.3em]",
    }[size];
</script>

<div class="flex flex-col items-center gap-1">
    <h1 class="milliways font-black uppercase {titleClass}">MILLIWAYS</h1>
    {#if size !== "sm"}
        <p class="subtitle uppercase {subtitleClass}">The Restaurant at the End of the Universe</p>
    {/if}
</div>

<style>
    .milliways {
        background: linear-gradient(to right, #e879f9, #4ade80, #a78bfa);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        filter:
            drop-shadow(0 0 8px rgba(232, 121, 249, 0.9))
            drop-shadow(0 0 20px rgba(232, 121, 249, 0.6))
            drop-shadow(0 0 40px rgba(167, 139, 250, 0.4));
    }

    .subtitle {
        color: #4ade80;
        text-shadow:
            0 0 7px #4ade80,
            0 0 15px #4ade80,
            0 0 30px #4ade80;
    }
</style>
