<script lang="ts">
	// src/routes/admin/[crud]/[operation]/+page.svelte

	// This is a custom Svelte store created by SvelteKit,
	//   it points to an instance of a Page object,
	//   which can allow us to gather data from the current page,
	//   such as the window.URL object, or the dynamic parameters of your route.
	// More details about the "page" store there:
	//   https://kit.svelte.dev/docs/modules#$app-stores-page
	import { page } from '$app/stores';

	// Same here as the previous "page" store, but the "browser" var contains
	//   a boolean that is set to "false" during server-side rendering, and to
	//   "true" when the Svelte component is mounted to the DOM.
	import { browser } from '$app/environment';

	// This function helps retrieving the [crud] and [operation] variables from the URL,
	// as well as the potential query string params like "?id=..."
	import { getRequestParams } from '@orbitale/svelte-admin';

	// That's your custom dashboard!
	// The "$lib" alias is configured by SvelteKit,
	//   it always points to your "src/lib/" directory.
	import { dashboard } from '$lib/Dashboard';

	// The "$:" syntax is valid Javascript code that tells Svelte
	//   that the following code is reactive, based on the values it depends on.
	// On this code, reactivity depends on "page" and "browser" variables.
	$: crud = $page.params.crud;
	$: operation = $page.params.operation;
	$: requestParameters = getRequestParams($page, browser);
	// Note: prefixing "page" with "$" makes sure we refer to the store's actual value.
	// If we didn't add this "$" prefix, we would use an object containing a method ".subscribe()", but we can use it to execude code whenever the store data changes. The "$" prefix sort of shortens everything for us automatically.
</script>

<!--
The "key" block makes sure its content is re-rendered whenever its arguments change.
Then, if the "$page" changes, the <svelte:component> component is re-rendered,
which is exactly what we expect when the current web page actually changes!
-->
{#key $page}
	<svelte:component
		this="{dashboard.theme.dashboard}"
		{dashboard}
		{crud}
		{operation}
		{requestParameters}
	/>
{/key}