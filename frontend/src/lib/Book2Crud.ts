
// SvelteAdmin classes:
import {
	CallbackAction,
	CallbackStateProcessor,
	CallbackStateProvider,
	CrudDefinition,
	DateField,
	DateRangeFilter,
	Delete,
	Edit,
	List,
	New,
	PaginatedResults,
	TextareaField,
	TextField,
	TextFilter,
	type RequestParameters,
	UrlAction,
	View, NumberField
} from '@orbitale/svelte-admin';

import { faker } from '@faker-js/faker';

import Pen from 'carbon-icons-svelte/lib/Pen.svelte';
import Flash from "carbon-icons-svelte/lib/Flash.svelte";
import TrashCan from 'carbon-icons-svelte/lib/TrashCan.svelte';
import ViewIcon from 'carbon-icons-svelte/lib/View.svelte';
import type { Book } from '$lib/internal/booksInternal';

export type Book2 = {
	id: number | string;
	title: string;
	author: string;
	publisher: string;
	isbn13: number;
	publication_year: number | string;
	abstract: string;
	language: string;
	format: string;
	url: string;
};

const fields = [
	new TextField('title', 'Title', { placeholder: "Enter the book's title", sortable: true }),
	new TextareaField('abstract', 'Abstract', {
		placeholder: "Enter the book's descrption",
		help: "Please don't make a summary of the book, remember to not spoil your readers!"
	}),
	new TextField('author', 'Author', { placeholder: "Enter the book's author", sortable: true }),
	new TextField('publisher', 'Publisher', { placeholder: "Enter the book's publisher", sortable: true }),
	new NumberField('isbn13', 'ISBN')
];

// const IdField = new TextField('string', 'ID');

const itemsPerPage = 10;

function randomWait(maxMilliseconds: number) {
	return new Promise((resolve: (...args: unknown[]) => unknown) =>
		setTimeout(resolve, Math.random() * maxMilliseconds)
	);
}

async function getBooks(): Promise<Array<Book2>> {
	if (typeof window === 'undefined') {
		return [];
	}

	const response = await fetch('http://localhost:8000/books');
	// Watch : If a object as a null value, could cause problem with crud CallbackStateProvider
	let items = <Array<Book2>> await response.json()

	let entities = items.map((value, index, array) => (
		{
			id: index,
			title: value.title,
			abstract: value.abstract,
			author: value.author,
			publisher: value.publisher,
			isbn13: value.isbn13,
			publication_year: value.publication_year,
			language: value.language,
			format: value.format,
			url: value.url,
		}));


	return entities;
}

function truncate(str: string, n: number, useWordBoundary: boolean = true) {
	if (str.length <= n) {
		return str;
	}
	const subString = str.slice(0, n - 1); // the original check
	return (
		(useWordBoundary ? subString.slice(0, subString.lastIndexOf(' ')) : subString) + ' ...'
	);
}

// Note: these fields can of course change based on different pages/actions,
//   so feel free to spread this out if you have more complex admins!

// Finally: the actual Crud object!
export const bookCrud2 = new CrudDefinition<Book2>({
	name: 'books2',
	label: { singular: 'Book', plural: 'Books' },
	// minStateLoadingTimeMs: 400,

	operations: [
		new List(
			[...fields],
			[
				new UrlAction('Edit', '/admin/books/edit', Pen),
				new UrlAction('Delete', '/admin/books/delete', TrashCan)
			],
			{
				}
		),
		new View([...fields]),
		new New(fields),
		new Edit(fields),
		new Delete(fields, new UrlAction('List', '/admin/books/list'))
	],

	stateProcessor: new CallbackStateProcessor(function (
		data,
		operation,
		requestParameters: RequestParameters = {}
	) {
		// if (operation.name === 'delete') {
		// 	const id = (requestParameters.id || '').toString();
		// 	getStorage().remove(id);
		//
		// 	return Promise.resolve();
		// }
		//
		// if (operation.name === 'edit' || operation.name === 'new') {
		// 	const id =
		// 		operation.name === 'edit' ? (requestParameters.id || '').toString() : faker.string.uuid();
		// 	const entity = data as Book2;
		// 	entity.id = id;
		//
		// 	if (operation.name === 'new') {
		// 		getStorage().add(entity);
		// 	} else {
		// 		getStorage().update(entity);
		// 	}
		//
		// 	return Promise.resolve();
		// }

		console.error('StateProcessor error: Unsupported Books Crud action "' + operation.name + '".');

		return Promise.resolve();
	}),

	stateProvider: new CallbackStateProvider<Book2>(async function (
		operation,
		requestParameters: RequestParameters = {}
	) {
		console.info('Books provider called', { operation: operation.name, requestParameters });

		if (operation.name === 'list') {
			const page = parseInt((requestParameters.page || '1').toString());
			if (isNaN(page)) {
				throw new Error(`Invalid "page" value: expected a number, got "${page}".`);
			}

			let entities = await getBooks();

			// Reduce abstact lenght
			entities.forEach((book) => {
				book.abstract = truncate(book.abstract, 200);
			})

			const listEntities = entities.slice(itemsPerPage * (page - 1), itemsPerPage * page);

			return new PaginatedResults(
				page,
				Math.ceil(entities.length / itemsPerPage),
				entities.length,
				listEntities
			);
		}

		// if (operation.name === 'edit' || operation.name === 'view') {
		// 	return Promise.resolve(getStorage().get((requestParameters?.id || '').toString()));
		// }
		//
		// if (operation.name === 'entity_view') {
		// 	return Promise.resolve(getStorage().get((requestParameters?.field_value || '').toString()));
		// }
		//
		// if (operation.name === 'entity_list') {
		// 	return Promise.resolve(getStorage().all());
		// }

		console.error('StateProvider error: Unsupported Books Crud action "' + operation.name + '".');

		return Promise.resolve(null);
	})
});
