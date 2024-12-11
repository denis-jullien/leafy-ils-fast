<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { get } from 'svelte/store';
	import { formula } from 'svelte-formula';
	import { checkPasswordScore } from '$lib/password';
	import { showNotification, Button } from 'saraui';

	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	let token: string | null = null;
	let email: string | null = null;

	onMount(() => {
		token = $page.url.searchParams.get('token');
		email = $page.url.searchParams.get('email');
	});

	const dispatch = createEventDispatcher();

	const {
		form,
		dirty,
		enrichment,
		formValidity,
		formValues,
		isFormValid,
		submitValues,
		touched,
		validity,
		initialValues
	} = formula({
		enrich: {
			password: {
				passwordStrength: (value) => checkPasswordScore(value)
			}
		},

		formValidators: {
			passwordsMatch: (values) =>
				values.password === values.passwordMatch ? null : 'Your passwords must match'
		}
	});

	$: usernameErr = $touched?.username && $validity?.username?.invalid;
	$: passwordErr = $touched?.password && $validity?.password?.invalid;
	$: passwordsMatchErr = $touched.passwordMatch && $formValidity?.passwordsMatch;
	$: passwordStrength = $enrichment?.password?.passwordStrength || 0;

	async function onSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		const user = get(submitValues);

		const response = await fetch(event.currentTarget.action, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				token: token,
				password: user.password
			})
		});

		// https://fastapi-users.github.io/fastapi-users/10.1/usage/routes/#post-reset-password
		if (response.ok) {
			console.log('OK');
		} else if (response.status === 422) {
			showNotification('error', '422 Validation Error');
		} else if (response.status === 400) {
			const details = await response.json();
			if (details.detail == 'RESET_PASSWORD_BAD_TOKEN') {
				showNotification('error', 'Bad or expired token');
			} else if (details.detail.code == 'REGISTER_INVALID_PASSWORD') {
				showNotification('error', 'Password validation failed' + details.detail.reason);
			}
			console.log(details);
		}

		console.log(response);
	}
</script>

<div class="flex flex-col gap-6 rounded-box bg-base-200 p-6 max-w-md text-center grow">
	<h1 class="text-2xl font-bold">New password</h1>

	<span> Enter your new password below to reset your password </span>

	<form
		class="flex flex-col gap-4"
		use:form
		id="signup"
		action="/auth/reset-password"
		on:submit|preventDefault={onSubmit}
	>
		<!--		<div hidden={$isFormValid}>-->
		<!--			There are errors-->
		<!--		</div>-->

		<!--		[DOM] Password forms should have (optionally hidden) username fields for accessibility: (More info: https://goo.gl/9p2vKq)-->
		<input id="username" type="email" value={email} hidden={true} autocomplete="username" />

		<label class="form-control">
			<div class="label">
				<span class="label-text">Password</span>
			</div>
			<input
				class="input input-bordered"
				type="password"
				id="password"
				name="password"
				autocomplete="new-password"
				required
				minlength="8"
				class:input-error={passwordErr}
			/>
			<div class="label" class:invisible={!passwordErr}>
				<span class="label-text-alt">{$validity?.password?.message}</span>
			</div>

			<meter
				class="progress"
				value={$enrichment?.password?.passwordStrength || 0}
				min="0"
				max="100"
				low="33"
				high="66"
				optimum="80"
			></meter>
		</label>

		<label class="form-control">
			<div class="label">
				<span class="label-text">Password Match</span>
			</div>

			<input
				class="input input-bordered"
				type="password"
				id="passwordMatch"
				name="passwordMatch"
				autocomplete="new-password"
				required
				minlength="8"
				class:input-error={passwordsMatchErr}
			/>
			<div class="label" class:invisible={!passwordsMatchErr}>
				<span class="label-text-alt">{$formValidity?.passwordsMatch}</span>
			</div>
		</label>

		<button class="btn btn-primary" type="submit" disabled={!$isFormValid}>Nex password</button>
	</form>
</div>
