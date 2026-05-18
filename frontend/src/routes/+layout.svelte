<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { User } from '$lib/types';

	let { children } = $props();

	let user = $state<User | null>(null);
	let authLoading = $state(true);

	onMount(async () => {
		try {
			user = await api.auth.me();
		} catch {
			user = null;
		}
		authLoading = false;
	});

	async function logout() {
		await api.auth.logout();
		user = null;
	}
</script>

<div class="min-h-screen flex flex-col">
	<nav class="border-b border-gray-200 px-6 py-3 flex items-center gap-6">
		<a href="/" class="font-bold text-lg tracking-tight mr-auto">Milliways</a>

		<div class="hidden sm:flex items-center gap-5">
			<a href="/" class="text-sm text-gray-600 hover:text-gray-900">Recipes</a>
			<a href="/shopping" class="text-sm text-gray-600 hover:text-gray-900">Shopping</a>
			<a href="/recipes/new" class="text-sm bg-gray-900 text-white px-3 py-1.5 rounded-md hover:bg-gray-700">
				+ New
			</a>
		</div>

		<div class="flex items-center gap-3 text-sm">
			{#if authLoading}
				<span class="text-gray-400">...</span>
			{:else if user}
				<span class="text-gray-500 hidden sm:inline">{user.name}</span>
				<button onclick={logout} class="text-gray-500 hover:text-gray-900">Log out</button>
			{:else}
				<a href={api.auth.loginUrl} class="text-gray-700 hover:text-gray-900 font-medium">
					Login with Google
				</a>
			{/if}
		</div>
	</nav>

	<main class="flex-1 px-6 py-8 max-w-3xl mx-auto w-full">
		{@render children()}
	</main>
</div>
