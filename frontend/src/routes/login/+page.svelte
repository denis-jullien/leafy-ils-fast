<script lang="ts">
	import AppShell from '$lib/AppShell.svelte';
	import { invalidateAll, goto } from '$app/navigation';
	import { deserialize, applyAction } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
	import type { Book2 } from '$lib/Book2Crud';
	// import type { ActionData } from './$types';
	//
	// let { form }: { form: ActionData } = $props();

	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement}) {
		const data = new FormData(event.currentTarget);

		const response = await fetch(event.currentTarget.action, {
			method: 'POST',
			body: data
		});

		if (response.ok) {
			console.log(response);

			const response2 = await fetch("/users/me");
			console.log(response2);
			const json = await response2.json()
			console.log(json);
			// goto("/admin", { invalidateAll: true })
			// return;
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

<AppShell>
<div class="flex justify-center mt-10">
	<div class="flex flex-col gap-4 rounded-box bg-base-200 p-6 max-w-md grow">
		<h1 class="text-3xl font-bold self-center">Log in</h1>

		<span class="self-center">
            Don't have an account?
            <a class="link link-secondary">Register</a>
        </span>

		<a class="btn btn-neutral">
			<i class="fa-brands fa-google text-primary"></i>
			Log in with Google
		</a>

		<div class="divider">OR</div>

		<form class="flex flex-col gap-4" method="POST" action="/auth/cookie/login" on:submit|preventDefault={handleSubmit}>

			<label class="form-control">
				<div class="label">
					<span class="label-text">Email</span>
				</div>

				<input class="input input-bordered" type="email" name="username" value="user@example.com"/>
			</label>

			<label class="form-control">
				<div class="label">
					<span class="label-text">Password</span>
					<a class="label-text link link-accent">Forgot password?</a>
				</div>

				<input type="password" name="password" class="input input-bordered" value="string"/>
			</label>

			<div class="form-control">
				<label class="cursor-pointer label self-start gap-2">
					<input type="checkbox" class="checkbox" />
					<span class="label-text">Remember me</span>
				</label>
			</div>

			<button id="button-login" class="btn btn-primary" hx-post="/auth/cookie/login">Log in</button>
		</form>
	</div>
</div>
</AppShell>