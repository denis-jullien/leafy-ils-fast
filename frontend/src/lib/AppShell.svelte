<script lang='ts'>
	import '../app.css';

	import '@fortawesome/fontawesome-free/css/all.min.css'

	import { SaraProvider } from "saraui"
</script>

<SaraProvider>
	<!-- minimun height of full screen-->
	<div class="flex flex-col h-screen justify-between">

		<div id="navbar" class="py-4 w-11/12 mx-auto" >

			<div class="flex flex-col">
				<!-- Top navbar (always visible) -->
				<nav class="navbar justify-between gap-4 bg-base-100 no-animation">
					<!-- Logo -->
					<a class="btn btn-ghost text-lg" href="/">
						<img alt="Logo" src="/images/logo.svg" class="w-8"/>
						Leafy ILS
					</a>

					<!-- Search -->
					<div class="join w-full max-w-xl hidden sm:inline-flex">
						<!-- Search options -->
						<select class="select  select-bordered join-item">
							<option selected>Good potions</option>
							<option>Bad potions</option>
							<option>Illegal potions</option>
						</select>

						<!-- Search input -->
						<input class="join-item input  input-bordered w-full" type="text" placeholder="Search">

						<!-- Search button -->
						<button class="join-item btn  btn-primary text-success-content">
							<i class="fa fa-search" aria-hidden="true"></i>
						</button>
					</div>

					<!-- Menu (Desktop) -->
					<div class="shrink-0 hidden md:flex gap-2">


						<a class="btn btn-md btn-ghost" href="">Create Book</a>
						<a class="btn btn-md btn-secondary" href="/admin" data-sveltekit-reload>Admin</a>
						<a class="btn btn-md btn-primary" href="/login">
							Log in
							<i class="fa-solid fa-right-to-bracket" aria-hidden="true"></i>
						</a>
					</div>

					<!-- Menu (Mobile) -->
					<div class="dropdown dropdown-end md:hidden">
						<button class="btn btn-ghost">
							<i class="fa-solid fa-bars text-lg"></i>
						</button>

						<ul tabindex="0" class="dropdown-content menu z-[1] bg-base-200 p-4 rounded-box shadow w-56 gap-2">
							<li><a>Create Account</a></li>
							<a class="btn btn-primary btn-sm">
								Log in
								<i class="fa fa-arrow-right text-xs" aria-hidden="true"></i>
							</a>
						</ul>
					</div>
				</nav>

				<!-- Botton navbar (mobile only) -->
				<nav class="navbar sm:hidden bg-base-200 border-neutral">
					<!-- Search -->
					<div class="join w-full">
						<!-- Search options -->
						<select class="select select-sm select-bordered join-item">
							<option selected>Good potions</option>
							<option>Bad potions</option>
							<option>Illegal potions</option>
						</select>

						<!-- Search input -->
						<input class="join-item input input-sm input-bordered w-full" type="text" placeholder="Search">

						<!-- Search button -->
						<button class="join-item btn btn-sm btn-primary text-success-content">
							<i class="fa fa-search" aria-hidden="true"></i>
						</button>
					</div>
				</nav>
			</div>
		</div>

		<div id="content">
			<slot />
		</div>

		<footer class="p-10 mt-10 sticky top-[100vh] bg-base-200 text-base-content text-base rounded">

			<!-- Link grid -->
			<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
				<nav class="flex flex-col">
					<h3 class="text-lg footer-title">Products</h3>
					<a class="link link-hover">Potion of AI</a>
					<a class="link link-hover">Healing potion</a>
					<a class="link link-hover">Potion of money</a>
					<a class="link link-hover">Potion of infinite coffee</a>
					<a class="link link-hover">Potion bundle</a>
				</nav>
				<nav>
					<div class="flex flex-col">
						<h3 class="text-lg footer-title">Features</h3>
						<a class="link link-hover">Learn potion history</a>
						<a class="link link-hover">Make your own potion</a>
						<a class="link link-hover">Experiment on humans</a>
						<a class="link link-hover">Mixing chemicals guide</a>
						<a class="link link-hover">Bring your own potions</a>
					</div>
				</nav>
				<nav>
					<div class="flex flex-col">
						<h3 class="text-lg footer-title">Resources</h3>
						dgqdsfgsdfgsdfgdqsfghsgfhgfjhh
						hhsgfhdg
						sgfdhgfh
						sgfh
					</div>
				</nav>
				<nav>
					<div class="flex flex-col">
						<h3 class="text-lg footer-title">Company</h3>
						<a class="link link-hover">News</a>
						<a class="link link-hover">Careers</a>
						<a class="link link-hover">Contact</a>
						<a class="link link-hover">Referrals</a>
						<a class="link link-hover">Meet the team</a>
					</div>
				</nav>
			</div>

			<div class="divider"></div>

			<!-- Bottom bar -->
			<aside class="flex flex-col sm:flex-row gap-6 justify-center sm:justify-between items-center">

				<!-- Brand -->
				<div class="flex items-center gap-4">
					<img alt="Logo" src="/images/logo.svg" class="w-8" />
					<div>
						<p class="text-2xl">Lecteurs des Arbousiers</p>
						<small>Copyright © 2024 - All rights reserved</small>
					</div>
				</div>

				<!-- Socials -->
				<nav class="flex gap-4">
					<a class="btn btn-ghost btn-sm btn-circle">
						<i class="fa-brands fa-github text-2xl"></i>
					</a>
					<a class="btn btn-ghost btn-sm btn-circle">
						<i class="fa-brands fa-twitter text-2xl"></i>
					</a>
					<a class="btn btn-ghost btn-sm btn-circle">
						<i class="fa-brands fa-facebook text-2xl"></i>
					</a>
					<a class="btn btn-ghost btn-sm btn-circle">
						<i class="fa-brands fa-youtube text-2xl"></i>
					</a>
				</nav>
			</aside>
		</footer>
	</div>
</SaraProvider>