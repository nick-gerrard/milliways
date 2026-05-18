<script lang="ts">
	import "../app.css";
	import Navbar from "$lib/components/Navbar.svelte";
	let { children } = $props();
</script>

<div
	class="fixed inset-0 -z-10"
	style="background: linear-gradient(135deg, #080010 0%, #1a0035 30%, #ff00aa33 50%, #00ff8833 60%, #0d001f 85%, #000008 100%)"
/>
<Navbar />

<main class="w-full p-4">
    {@render children()}
</main>
