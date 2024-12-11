<script lang="ts">
	import UnorderedList from 'carbon-components-svelte/src/UnorderedList/UnorderedList.svelte';
	import LogoGithub from 'carbon-icons-svelte/lib/LogoGithub.svelte';
	import { _ } from 'svelte-i18n';

	import { initLocale } from '@orbitale/svelte-admin';
	import { dashboard } from '$lib/Dashboard';
	import fr from '$lib/translations/fr';

	initLocale('fr', { fr });

	import '@carbon/charts-svelte/styles.css';
	import { BarChartSimple } from '@carbon/charts-svelte';
	import { Tile } from 'carbon-components-svelte';
</script>

<svelte:component this={dashboard.theme.dashboard} {dashboard}>
	<h1>Svelte Admin demo app</h1>

	<p>
		Svelte Admin is a (currently prototype) admin generator delivered as a Typescript library and a
		set of Svelte components as rendering system.
	</p>

	<p>
		If you detect any bug in this demo, feel free to clone the project or submit an issue in the
		<a href="https://github.com/Orbitale/SvelteAdmin"><LogoGithub />&nbsp;Github Repository</a>!
	</p>

	<p>Here are the available CRUDs for the demo app:</p>

	<UnorderedList expressive={true}>
		{#each dashboard.cruds as crud}
			<li>
				<a href="/admin/{crud.name}/{crud.options.defaultOperationName}">
					{$_(crud.options.label.plural)}
				</a>
			</li>
		{/each}
	</UnorderedList>

	<Tile>
		<h1>Svelte Admin charts</h1>
		<!--		https://github.com/carbon-design-system/carbon-charts/tree/master/packages/svelte-->
		<BarChartSimple
			data={[
				{ group: 'Qty', value: 65000 },
				{ group: 'More', value: 29123 },
				{ group: 'Sold', value: 35213 },
				{ group: 'Restocking', value: 51213 },
				{ group: 'Misc', value: 16932 }
			]}
			options={{
				title: 'Simple bar (discrete)',
				height: '400px',
				axes: {
					left: { mapsTo: 'value' },
					bottom: { mapsTo: 'group', scaleType: 'labels' }
				}
			}}
		/>
	</Tile>
</svelte:component>

<style>
	li {
		list-style-type: disc;
		list-style-position: inside;
	}
</style>
