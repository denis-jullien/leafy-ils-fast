<script lang="ts">
	import '../../../admin.css';

	import UnorderedList from 'carbon-components-svelte/src/UnorderedList/UnorderedList.svelte';
	import LogoGithub from 'carbon-icons-svelte/lib/LogoGithub.svelte';
	import { _ } from 'svelte-i18n';

	import { writable } from 'svelte/store';

	import { Tile } from 'carbon-components-svelte';
	import { DataTable, Link } from 'carbon-components-svelte';
	import Launch from 'carbon-icons-svelte/lib/Launch.svelte';
	import { Tabs, Tab, TabContent } from 'carbon-components-svelte';

	import { Form, FormGroup, TextInput, TextArea, Button } from 'carbon-components-svelte';

	import { InlineNotification } from 'carbon-components-svelte';
	import { ButtonSet, InlineLoading } from 'carbon-components-svelte';
	import { onDestroy, onMount } from 'svelte';
	import { Select, SelectItem } from "carbon-components-svelte";
	import { ImageLoader } from "carbon-components-svelte";



	import { initLocale } from '@orbitale/svelte-admin';
	import { dashboard } from '$lib/Dashboard';
	import fr from '$lib/translations/fr';
	import Pen from 'carbon-icons-svelte/lib/Pen.svelte';
	import TrashCan from 'carbon-icons-svelte/lib/TrashCan.svelte';

	import QrCodeScanner from '$lib/QrCodeScanner.svelte';
	import { Grid, Row, Column, Content, TileGroup, RadioTile } from 'carbon-components-svelte';
	import type { BookCreate, BookPublic } from '$lib/apiTypes';




	import {
		ComposedModal,
		ModalHeader,
		ModalBody,
		ModalFooter,
		Checkbox
	} from 'carbon-components-svelte';

	import { ToastNotification } from 'carbon-components-svelte';
	import { fade } from 'svelte/transition';

	// import { continents, countries, languages } from 'countries-list'

	import * as languages  from "@cospired/i18n-iso-languages"
	import * as english from "@cospired/i18n-iso-languages/langs/en.json"
	import * as french from "@cospired/i18n-iso-languages/langs/fr.json"

	let langs = {}

	onMount(() => {
		// Support french & english languages.
		languages.registerLocale(english);
		languages.registerLocale(french);

		langs = languages.getNames("fr")
		console.log(langs)
	})


	let timeout = undefined;
	$: showNotification = timeout !== undefined;
	let errotText: string;

	let open = false;
	let checked = false;

	let previewWidth;
	let mediaErrorMessage = '';
	let w = 400;

	function onQRScan(event: CustomEvent) {
		alert(event.detail.qrContent);
	}

	initLocale('fr', { fr });

	let isbn = '';
	let bar = 'qux';
	let result: Array<Book2> = [];
	let scanpause = false;

	let currentBook: BookPublic = {};
	let error = null;

	let submitstate = 'dormant';
	const descriptionMap = {
		active: 'Submitting...',
		finished: 'Success',
		inactive: 'Cancelling...'
	};

	async function doPost() {
		submitstate = 'active';

		const res = await fetch('/api/v1/records/' + isbn, {
			method: 'POST'
		});

		if (res.status === 400) {
			submitstate = 'error';
			errotText = (await res.json()).detail;
			timeout = 3_000; // 3 seconds
		} else if (res.status === 200) {
			submitstate = 'finished';
			const json = <BookCreate>await res.json();
			console.log(json);

			currentBook = json;
			open = true;
			submitstate = 'dormant';
		} else {
			submitstate = 'dormant';
		}
		isbn = '';
	}

	async function doCreate() {
		console.log('Create new book');
		const res = await fetch('/api/v1/books', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(currentBook)
		});

		const json = <BookPublic>await res.json();
		console.log(json);

		result = [json, ...result];
		scanpause = false;
	}



	async function doPost2(isbn: string) {
		scanpause = true;
		const res = await fetch('/api/v1/books/' + isbn, {
			method: 'POST'
		});

		const json = <BookCreate>await res.json();
		json.id = Math.random().toString(36).substr(2, 10);
		console.log(json);
		isbn = '';
		result = [json, ...result];

		scanpause = false;
	}

	function handleClick() {
		result = result.slice(1);
	}

	let modalform;
	let modalformbutton;
	let formElement;


</script>

<svelte:component this={dashboard.theme.dashboard} {dashboard}>
	<Content>
		<Grid>
			<Row>
				<Column>
					<h1>HeaderSwitcher</h1>
					<p>
						Select a transition option below and click on the App Switcher icon in the top right.
					</p>

					<Tile>
						<Tabs type="container">
							<Tab label="Tab label 1" />
							<Tab label="Tab label 2" />
							<Tab label="Tab label 3" />
							<svelte:fragment slot="content">
								<TabContent>
									<p>Plopopd</p>

									<Form on:submit={doPost}>
										<FormGroup>
											<TextInput
												bind:value={isbn}
												labelText="User name"
												placeholder="Enter user name..."
												required
												autofocus
											/>
										</FormGroup>
										<ButtonSet>
											<Button type="submit" disabled={submitstate === 'active'}>Submit</Button>
											{#if submitstate !== 'dormant'}
												<InlineLoading
													status={submitstate}
													description={descriptionMap[submitstate]}
												/>
											{/if}
										</ButtonSet>
									</Form>
								</TabContent>
								<TabContent>
									<h1>Mobile scan</h1>
									<div class="barcode-scanner">
										<!--						<QrCodeScanner-->
										<!--							scanSuccess={(e) => {console.log(e)}}-->
										<!--							scanFailure={(e) => {console.log(e)}}-->
										<!--							paused={false}-->
										<!--							width={320}-->
										<!--							height={320}-->
										<!--							class="w-full max-w-sm bg-slate-700 rounded-lg overflow-hidden"-->
										<!--						/>-->
										<QrCodeScanner
											on:detect={(e) => doPost2(e.detail.decodedText)}
											paused={scanpause}
											width={320}
											height={320}
											class="w-full max-w-sm bg-slate-700 rounded-lg overflow-hidden"
										/>
									</div>

									<style>
										.barcode-scanner {
											width: 100%;
											max-width: 384px;
											aspect-ratio: 1;
										}
									</style>
								</TabContent>
								<TabContent>Content 3</TabContent>
							</svelte:fragment>
						</Tabs>
					</Tile>
				</Column>
			</Row>

			{#if showNotification}
				<div transition:fade>
					<InlineNotification
						{timeout}
						kind="error"
						title="Error"
						subtitle={errotText}
						on:close={(e) => {
							timeout = undefined;
							console.log(e.detail.timeout); // true if closed via timeout
						}}
					/>
				</div>
			{/if}

			<Row style="padding-top: 10px;">
				<Column>
					{#if result.length > 0}
						<DataTable
							headers={[
								{ key: 'name', value: 'Name' },
								{ key: 'author', value: 'Author' },
								{ key: 'publisher', value: 'Publisher' },
								{ key: 'rule', value: '' }
							]}
							rows={result.map((book) => ({
								id: book.id,
								name: book.title,
								author: book.author,
								publisher: book.publisher,
								rule: book.id
							}))}
						>
							<strong slot="title">Results</strong>
							<span slot="description" style="font-size: 1rem"> Historique des résultats </span>
							<svelte:fragment slot="cell" let:row let:cell>
								{#if cell.key === 'rule'}
									{#if row.name === undefined}
										<InlineNotification
											hideCloseButton
											lowContrast
											kind="error"
											title="Error:"
											subtitle="Item not found."
										/>
									{:else}
										<Link icon={Pen} href="/admin/books/edit?id={cell.value}">Edit</Link>
										<Link icon={TrashCan} href="/admin/books/delete?id={cell.value}">Delete</Link>
									{/if}
								{:else}
									{cell.value}
								{/if}
							</svelte:fragment>
						</DataTable>
					{/if}
				</Column>
			</Row>
		</Grid>
	</Content>
</svelte:component>

<ComposedModal bind:open on:submit={() => formElement.requestSubmit()} preventCloseOnClickOutside size="lg">
	<ModalHeader label="Changes" title="Confirm changes" />
	<ModalBody hasForm>
		<Grid fullWidth>
			<Row>
				<Column>

		<div class="w-72 mx-auto	">
		<ImageLoader
			src={currentBook.cover}
		>
			<svelte:fragment slot="loading">
				<InlineLoading />
			</svelte:fragment>
			<svelte:fragment slot="error">An error occurred.</svelte:fragment>
		</ImageLoader>
		</div>
		</Column>
				<Column>
		<form
			on:submit={() => {
				doCreate().then(value => {open = false})

			}}
			bind:this={formElement}
		>
			<FormGroup>
				{#if currentBook}
					<TextInput
						bind:value={currentBook.title}
						labelText="Title"
						placeholder="Enter user name..."
						required
					/>
					<TextInput
						bind:value={currentBook.author}
						labelText="Author"
						placeholder="Enter user name..."
						required
					/>

					<TextArea
						bind:value={currentBook.abstract}
						labelText="App description"
						placeholder="Enter a description..."
					/>

					<TextInput
						bind:value={currentBook.publisher}
						labelText="publisher"
						placeholder="Enter user name..."
						required
					/>

					<TextInput
						bind:value={currentBook.format}
						labelText="format"
						placeholder="Enter user name..."
						required
					/>

					<TextInput
						bind:value={currentBook.publication_date}
						labelText="publication_date"
						placeholder="Enter user name..."
						required
					/>

					<TextInput
						bind:value={currentBook.cover}
						labelText="couverture"
						placeholder="Enter user name..."
					/>

					<Select
						labelText="language"
						bind:selected={currentBook.language}
					>
						{#each Object.entries(langs) as [title, paragraph]}
						<SelectItem value="{title}" text="{paragraph}" />
						{/each}
						<SelectItem value="g10" text="Gray 10" />
						<SelectItem value="g80" text="Gray 80" />
						<SelectItem value="g90" text="Gray 90" />
						<SelectItem value="g100" text="Gray 100" />
					</Select>

					<TextInput
						bind:value={currentBook.isbn}
						labelText="isbn"
						disabled
					/>


				{/if}
			</FormGroup>
		</form>
				</Column>
			</Row>
		</Grid>
	</ModalBody>
	<ModalFooter
		primaryButtonText="Proceed"
		secondaryButtons={[{ text: 'Cancel' }]}
		on:click:button--secondary={({ detail }) => {
			if (detail.text === 'Cancel') open = false;
		}}
	/>
</ComposedModal>
