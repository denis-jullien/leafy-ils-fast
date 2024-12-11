<script lang="ts">
</script>

<aside
	class="flex flex-col items-center sticky top-0 overflow-y-auto space-y-4 w-72 py-6 px-4 bg-base-200 rounded-box"
>
	<!-- Logo -->
	<a class="btn btn-ghost text-lg">
		<img alt="Logo" src="/images/logo.svg" class="w-6" />
		Company Name
	</a>

	<img alt="Profile" src="/images/avatar.png" class="w-32 rounded-full" />

	<h2 class="font-bold text-lg">User name</h2>

	<span class="text-sm text-accent">username@email.com</span>

	<ul class="menu menu-lg w-full">
		<li>
			<a>
				<i class="fa-solid fa-inbox fa-fw"></i>
				Inbox
			</a>
		</li>
		<li>
			<a class="active">
				<i class="fa-solid fa-user fa-fw"></i>
				Accounts
			</a>
		</li>
		<li>
			<a>
				<i class="fa-solid fa-ticket fa-fw"></i>
				Tickets
			</a>
		</li>
		<li>
			<a>
				<i class="fa-solid fa-gear fa-fw"></i>
				Settings
			</a>
		</li>
	</ul>
</aside>

<!-- Card -->
<div class="flex flex-col gap-6 bg-base-200 rounded-box p-6 max-w-xl">
	<!-- Header -->
	<div class="flex justify-between items-center">
		<span class="text-sm">Jan 10, 2024</span>

		<a class="btn btn-sm btn-primary">Design</a>
	</div>

	<!-- Body -->
	<div class="flex flex-col gap-2">
		<a class="text-xl font-bold link"> Accessibility tools for designers and developers </a>

		<span>
			Lorem ipsum dolor sit, amet consectetur adipisicing elit. Tempora expedita dicta totam
			aspernatur doloremque. Excepturi iste iusto eos enim reprehenderit nisi, accusamus delectus
			nihil quis facere in modi ratione libero!
		</span>
	</div>

	<!-- Footer -->
	<div class="flex justify-between items-center">
		<a class="link link-accent">Read more</a>

		<a class="btn btn-ghost">
			<img alt="Profile" src="/images/avatar.png" class="w-8 rounded-full" />

			User name
		</a>
	</div>
</div>
