<script lang="ts">
	import { Modal } from 'saraui';

	let isOpen = false;

	async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
		const data = new FormData(event.currentTarget);
		const email = String(data.get('email'));
		console.log(data);

		const body = JSON.stringify({
			email: email
		});
		console.log(body);

		const response = await fetch(event.currentTarget.action, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: body
		});

		if (response.ok) {
			console.log(response);
			isOpen = true;
		}
	}

	async function handleCancel(e: Event) {
		isOpen = false;
	}
</script>

<div class="flex flex-col gap-6 rounded-box bg-base-200 p-6 max-w-md text-center">
	<h1 class="text-2xl font-bold">Forgot password?</h1>

	<span>
		Remember your password?
		<a class="link link-secondary" href="/login">Log in here</a>
	</span>

	<form
		class="flex flex-col gap-4"
		method="POST"
		action="/auth/forgot-password"
		on:submit|preventDefault={handleSubmit}
	>
		<label class="form-control">
			<div class="label">
				<span class="label-text">Email</span>
			</div>

			<input type="email" class="input input-bordered" name="email" autofocus />
		</label>

		<button class="btn btn-primary">Reset password</button>
	</form>
</div>

<Modal bind:isOpen>
	Used to shows a dialog element when clicked.
	<div class="modal-action">
		<form method="dialog">
			<button
				on:click={handleCancel}
				class="
            btn
            focus:outline-none
            focus:border-none
            active:border-none
            active:outline-none
        "
			>
				Close
			</button>
		</form>
	</div>
</Modal>
