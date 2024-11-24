<script lang="ts">
	import UnorderedList from 'carbon-components-svelte/src/UnorderedList/UnorderedList.svelte';
	import LogoGithub from 'carbon-icons-svelte/lib/LogoGithub.svelte';
	import { _ } from 'svelte-i18n';

	import { Tile } from "carbon-components-svelte";

	import {
		Form,
		FormGroup,
		Checkbox,
		RadioButtonGroup,
		RadioButton,
		Select,
		SelectItem,
		TextInput,
		Button,
	} from "carbon-components-svelte";


	import { initLocale } from '@orbitale/svelte-admin';
	import { dashboard } from '$lib/Dashboard';
	import fr from '$lib/translations/fr';

	initLocale('fr', { fr });
</script>

<svelte:component this={dashboard.theme.dashboard} {dashboard}>


	<Tile><h1>Svelte Admin books adding</h1>

	<p>
		Plopopd
	</p>

	<Form on:submit>
<!--		<FormGroup legendText="Checkboxes">-->
<!--			<Checkbox id="checkbox-0" labelText="Checkbox Label" checked />-->
<!--			<Checkbox id="checkbox-1" labelText="Checkbox Label" />-->
<!--			<Checkbox id="checkbox-2" labelText="Checkbox Label" disabled />-->
<!--		</FormGroup>-->
<!--		<FormGroup legendText="Radio buttons">-->
<!--			<RadioButtonGroup name="radio-button-group" selected="default-selected">-->
<!--				<RadioButton-->
<!--					id="radio-1"-->
<!--					value="standard"-->
<!--					labelText="Standard Radio Button"-->
<!--				/>-->
<!--				<RadioButton-->
<!--					id="radio-2"-->
<!--					value="default-selected"-->
<!--					labelText="Default Selected Radio Button"-->
<!--				/>-->
<!--				<RadioButton-->
<!--					id="radio-4"-->
<!--					value="disabled"-->
<!--					labelText="Disabled Radio Button"-->
<!--					disabled-->
<!--				/>-->
<!--			</RadioButtonGroup>-->
<!--		</FormGroup>-->
<!--		<FormGroup>-->
<!--			<Select id="select-1" labelText="Select menu">-->
<!--				<SelectItem-->
<!--					disabled-->
<!--					hidden-->
<!--					value="placeholder-item"-->
<!--					text="Choose an option"-->
<!--				/>-->
<!--				<SelectItem value="option-1" text="Option 1" />-->
<!--				<SelectItem value="option-2" text="Option 2" />-->
<!--				<SelectItem value="option-3" text="Option 3" />-->
<!--			</Select>-->
<!--		</FormGroup>-->
		<FormGroup>
			<TextInput labelText="User name" placeholder="Enter user name..." required autofocus/>
		</FormGroup>
		<Button type="submit">Submit</Button>
	</Form>
	</Tile>
</svelte:component>

