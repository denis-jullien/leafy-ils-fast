<script lang="ts">
	import AppShell from '$lib/AppShell.svelte';
	import { invalidateAll, goto } from '$app/navigation';
	import { deserialize, applyAction } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
	import type { Book2 } from '$lib/Book2Crud';
	// import type { ActionData } from './$types';
	//
	// let { form }: { form: ActionData } = $props();

	import { Loader } from 'saraui';

	let loading = false;
	let formError = false;

	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		formError = false;
		const data = new FormData(event.currentTarget);

		const response = await fetch(event.currentTarget.action, {
			method: 'POST',
			body: data
		});

		if (response.ok) {
			// const response2 = await fetch("/users/me");
			// console.log(response2);
			// const json = await response2.json()
			// console.log(json);
			goto('/account', { invalidateAll: true });
			// return;
		} else {
			formError = true;
		}

		// const result: ActionResult = deserialize(await response.text());
		//
		// if (result.type === 'success') {
		// 	// rerun all `load` functions, following the successful update
		// 	await invalidateAll();
		// }
		//
		// applyAction(result);
	}
</script>

<div class="flex flex-col gap-6 max-w-md grow">
	<div role="alert" class="alert alert-error" class:invisible={!formError}>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			class="h-6 w-6 shrink-0 stroke-current"
			fill="none"
			viewBox="0 0 24 24"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
			/>
		</svg>
		<span>Error! Task failed successfully.</span>
	</div>

	<div class="flex flex-col gap-4 rounded-box bg-base-200 p-6">
		<h1 class="text-3xl font-bold self-center">Log in</h1>

		<span class="self-center">
			Don't have an account?
			<a class="link link-secondary">Register</a>
		</span>

		<!--			<a class="btn btn-neutral">-->
		<!--				<i class="fa-brands fa-google text-primary"></i>-->
		<!--				Log in with Google-->
		<!--			</a>-->

		<!--			<div class="divider">OR</div>-->

		<form
			class="flex flex-col gap-4"
			method="POST"
			action="/auth/cookie/login"
			on:submit|preventDefault={handleSubmit}
		>
			<label class="form-control">
				<div class="label">
					<span class="label-text">Email</span>
				</div>

				<input class="input input-bordered" type="email" name="username" value="user@example.com" />
			</label>

			<label class="form-control">
				<div class="label">
					<span class="label-text">Password</span>
					<a class="label-text link link-accent" href="/login/reset">Forgot password?</a>
				</div>

				<input type="password" name="password" class="input input-bordered" value="string" />
			</label>

			<div class="form-control">
				<label class="cursor-pointer label self-start gap-2">
					<input type="checkbox" class="checkbox" />
					<span class="label-text">Remember me</span>
				</label>
			</div>

			<button id="button-login" class="btn btn-primary"
				>Log in
				{#if loading}
					<Loader />
				{/if}
			</button>
		</form>
	</div>
</div>
