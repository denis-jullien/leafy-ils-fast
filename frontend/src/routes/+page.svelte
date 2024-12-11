<script lang="ts">
	import AppShell from '$lib/AppShell.svelte';
	import type { Book } from '$lib/apiTypes';

	let elemMovies: HTMLDivElement;

	const unsplashIds = [
		'vjUokUWbFOs',
		'1aJuPtQJX_I',
		'Jp6O3FFRdEI',
		'I3C_eojFVQY',
		's0fXOuyTH1M',
		'z_X0PxmBuIQ'
	];
	const carouselBooks: Array<Book> = [
		{
			title: 'Moi, François le Français',
			author: 'Georges Piombo',
			publisher: 'Paris : Éditions Libre & Solidaire , 2022',
			isbn13: 9782377940820,
			publication_year: 2022,
			abstract:
				"La vie est une aventure. Ma mère et mon père, une histoire d'amour au-dessus de tout. Il l'a enlevée, ils",
			language: 'fr',
			format: '1 vol. (186 p.) ; 23 cm',
			url: 'https://images.unsplash.com/photo-1572826246393-e42b63b4ac82?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=256&w=256'
		},
		{
			title: "Je t'aimerai toujours, quoi qu'il arrive",
			author: 'Debi Gliori',
			publisher: 'Paris : Gautier-Languereau , impr. 2014',
			isbn13: 9782013944762,
			publication_year: 2014,
			abstract: '',
			language: 'fr',
			format: '1 vol. (non paginé [30] p.) : ill. en coul., couv. ill. en coul. ; 18 cm',
			url: 'https://images.unsplash.com/photo-1616607041376-2bf38ce4e71a?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
		},
		{
			title: 'La végétarienne',
			author: 'Han Kang',
			publisher: 'Paris : le Livre de poche , DL 2016',
			isbn13: 9782253067900,
			publication_year: 2016,
			abstract: '',
			language: 'fr',
			format: '1 volume (211 pages) : couverture illustrée ; 18 cm',
			url: 'https://images.unsplash.com/photo-1732287932412-6bd1916b19cd?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
		},
		{
			title: 'Moi, François le Français',
			author: 'Georges Piombo',
			publisher: 'Paris : Éditions Libre & Solidaire , 2022',
			isbn13: 9782377940820,
			publication_year: 2022,
			abstract:
				"La vie est une aventure. Ma mère et mon père, une histoire d'amour au-dessus de tout. Il l'a enlevée, ils",
			language: 'fr',
			format: '1 vol. (186 p.) ; 23 cm',
			url: 'https://images.unsplash.com/photo-1572826246393-e42b63b4ac82?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=256&w=256'
		},
		{
			title: "Je t'aimerai toujours, quoi qu'il arrive",
			author: 'Debi Gliori',
			publisher: 'Paris : Gautier-Languereau , impr. 2014',
			isbn13: 9782013944762,
			publication_year: 2014,
			abstract: '',
			language: 'fr',
			format: '1 vol. (non paginé [30] p.) : ill. en coul., couv. ill. en coul. ; 18 cm',
			url: 'https://images.unsplash.com/photo-1616607041376-2bf38ce4e71a?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
		},
		{
			title: 'La végétarienne',
			author: 'Han Kang',
			publisher: 'Paris : le Livre de poche , DL 2016',
			isbn13: 9782253067900,
			publication_year: 2016,
			abstract: '',
			language: 'fr',
			format: '1 volume (211 pages) : couverture illustrée ; 18 cm',
			url: 'https://images.unsplash.com/photo-1732287932412-6bd1916b19cd?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
		}
	];

	function multiColumnLeft(): void {
		let x = elemMovies.scrollWidth;
		if (elemMovies.scrollLeft !== 0) x = elemMovies.scrollLeft - elemMovies.clientWidth;
		elemMovies.scroll(x, 0);
	}

	function multiColumnRight(): void {
		let x = 0;
		// -1 is used because different browsers use different methods to round scrollWidth pixels.
		if (elemMovies.scrollLeft < elemMovies.scrollWidth - elemMovies.clientWidth - 1)
			x = elemMovies.scrollLeft + elemMovies.clientWidth;
		elemMovies.scroll(x, 0);
	}
</script>

<AppShell>
	<div
		class="hero mx-auto bg-[url('/images/annie-spratt-0ZPSX_mQ3xI-unsplash.jpg')] bg-center rounded-box w-11/12"
	>
		<div class="hero-overlay bg-opacity-60 rounded-box"></div>
		<div class="hero-content">
			<div class="max-w-full">
				<h1 class="mb-5 text-neutral-content text-center text-5xl font-bold">
					Nos livres du moment
				</h1>
				<!--		carrousel	-->

				<div class="grid grid-cols-[auto_1fr_auto] gap-4 items-center">
					<!-- Button: Left -->
					<button type="button" class="btn-icon variant-filled" on:click={multiColumnLeft}>
						<i class="fa-solid fa-arrow-left" />
					</button>
					<!-- Carousel -->
					<div
						bind:this={elemMovies}
						class="snap-x snap-mandatory scroll-smooth flex pb-2 overflow-x-auto"
					>
						{#each carouselBooks as cbook}
							<div class="shrink-0 w-[25%] snap-start">
								<div class="card bg-base-100 shadow-xl mx-6">
									<figure class="h-40">
										<img src={cbook.url} alt="Shoes" />
									</figure>
									<div class="card-body">
										<div class="badge badge-secondary">NEW</div>
										<h2 class="card-title">{cbook.title}</h2>
										<!--											<a href="/" class="block card card-hover mx-2">-->
										<!--												<img-->
										<!--													class="rounded-container-token hover:brightness-125"-->
										<!--													src="https://images.unsplash.com/photo-1572826246393-e42b63b4ac82?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=256&w=256"-->
										<!--													alt={unsplashId}-->
										<!--													title={unsplashId}-->
										<!--													loading="lazy"-->
										<!--												/>-->
										<!--											</a>-->
										<p>If a dog chews shoes whose shoes does he choose?</p>
										<div class="card-actions justify-end">
											<div class="badge badge-outline">{cbook.author}</div>
											<div class="badge badge-outline">{cbook.publication_year}</div>
										</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
					<!-- Button-Right -->
					<button type="button" class="btn-icon variant-filled" on:click={multiColumnRight}>
						<i class="fa-solid fa-arrow-right" />
					</button>
				</div>

				<!--		end carouseels	-->
			</div>
		</div>
	</div>

	<div class="flex justify-center my-10 max-w-7xl mx-auto">
		<div class="flex flex-col items-center text-center gap-6 w-full">
			<h1 class="font-bold text-3xl">
				Actualités
				<span class="text-primary">récentes</span>
			</h1>
			<div class="grid grid-cols-1 gap-4 w-full">
				<!--{% include "acticle_card.jinja" %}-->
				<!--{% include "acticle_card.jinja" %}-->
				<!--{% include "acticle_card.jinja" %}-->
				<!-- Card -->
				<div class="flex w-7xl">
					<!-- Image -->
					<div
						class="bg-[url('/images/pawel-czerwinski-Lki74Jj7H-U-unsplash.jpg')] bg-center rounded-box w-72"
					></div>

					<!-- Content -->
					<div class="flex flex-col gap-4 p-6 rounded-box w-full">
						<div class="flex items-center">
							<a class="btn btn-sm">Evenement</a>
						</div>
						<h1 class="font-bold text-xl text-left">Super titre</h1>

						<span class="text-justify">
							Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
							incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
							exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
							dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
							Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
							mollit anim id est laborum.
						</span>

						<div class="flex justify-between items-center">
							<span class="text-sm">10 novembre 2024</span>

							<a class="btn btn-primary btn-sm">Lire plus</a>
						</div>
					</div>
				</div>
			</div>
			<a class="btn btn-neutral">
				Lire tous les articles
				<i class="fa-solid fa-circle-arrow-right text-lg"></i>
			</a>
		</div>
	</div>
</AppShell>

<!--<style lang="postcss">-->
<!--    figure {-->
<!--        @apply flex relative flex-col;-->
<!--    }-->
<!--    figure svg,-->
<!--    .img-bg {-->
<!--        @apply w-64 h-64 md:w-80 md:h-80;-->
<!--    }-->
<!--    .img-bg {-->
<!--        @apply absolute z-[-1] rounded-full blur-[50px] transition-all;-->
<!--        animation: pulse 5s cubic-bezier(0, 0, 0, 0.5) infinite,-->
<!--        glow 5s linear infinite;-->
<!--    }-->
<!--    @keyframes glow {-->
<!--        0% {-->
<!--            @apply bg-primary-400/50;-->
<!--        }-->
<!--        33% {-->
<!--            @apply bg-secondary-400/50;-->
<!--        }-->
<!--        66% {-->
<!--            @apply bg-tertiary-400/50;-->
<!--        }-->
<!--        100% {-->
<!--            @apply bg-primary-400/50;-->
<!--        }-->
<!--    }-->
<!--    @keyframes pulse {-->
<!--        50% {-->
<!--            transform: scale(1.5);-->
<!--        }-->
<!--    }-->
<!--</style>-->
