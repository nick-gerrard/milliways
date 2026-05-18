<script lang="ts">
	import "../app.css";
	import Navbar from "$lib/components/Navbar.svelte";
	let { children } = $props();
</script>

<div
	class="fixed inset-0 -z-10 bg-slate-900 "></div>
    <!-- Blobs — fixed so they stay in the background across the whole page -->
    <div
      class="pointer-events-none fixed -top-32 -left-32 h-96 w-96 rounded-full bg-violet-600 opacity-20 blur-[100px]"
    ></div>
    <div
      class="pointer-events-none fixed -bottom-32 -right-32 h-96 w-96 rounded-full bg-pink-500 opacity-20 blur-[100px]"
    ></div>
    <div
      class="pointer-events-none fixed -top-32 -right-32 h-96 w-96 rounded-full bg-emerald-500 opacity-20 blur-[100px]"
    ></div>
    <div
      class="pointer-events-none fixed -bottom-32 -left-32 h-96 w-96 rounded-full bg-violet-800 opacity-20 blur-[100px]"
    ></div>
	<!-- style="background: linear-gradient(135deg, #080010 0%, #1a0035 30%, #ff00aa33 50%, #00ff8833 60%, #0d001f 85%, #000008 100%)" -->
<Navbar />

<main class="w-full p-4">
    {@render children()}
</main>
