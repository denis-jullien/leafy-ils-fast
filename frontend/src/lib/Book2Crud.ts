// SvelteAdmin classes:
import {
	CallbackAction,
	CallbackStateProcessor,
	CallbackStateProvider,
	CrudDefinition,
	Delete,
	Edit,
	List,
	New,
	NumberField,
	PaginatedResults,
	type RequestParameters,
	TextareaField,
	TextField,
	UrlAction,
	View
} from '@orbitale/svelte-admin';

import Pen from 'carbon-icons-svelte/lib/Pen.svelte';
import TrashCan from 'carbon-icons-svelte/lib/TrashCan.svelte';
import type { BookCreate, BookPublic } from '$lib/apiTypes';
import { MyApiInterface } from '$lib/internal/apiStorage';
import Flash from 'carbon-icons-svelte/lib/Flash.svelte';

// export type Book2 = {
// 	id: number | string;
// 	title: string;
// 	author: string;
// 	publisher: string;
// 	isbn13: number;
// 	publication_year: number | string;
// 	abstract: string;
// 	language: string;
// 	format: string;
// 	url: string;
// };
// export interface Book {
// 	title: string;
// 	author: string;
// 	publisher: string;
// 	isbn13: number;
// 	publication_year: number | string;
// 	abstract: string;
// 	language: string;
// 	format: string;
// 	url: string ;
// }
//
//
// export type Book2 = Book & {
// 	id: number | string;
// }



const fields = [
	new TextField('title', 'Title', { placeholder: "Enter the book's title", sortable: true }),
	new TextareaField('abstract', 'Abstract', {
		placeholder: "Enter the book's descrption",
		help: "Please don't make a summary of the book, remember to not spoil your readers!"
	}),
	new TextField('author', 'Author', { placeholder: "Enter the book's author", sortable: true }),
	new TextField('publisher', 'Publisher', { placeholder: "Enter the book's publisher", sortable: true }),
	new NumberField('isbn', 'ISBN')
];

// const IdField = new TextField('string', 'ID');

const itemsPerPage = 10;

let bookApi = new MyApiInterface<BookPublic>('/api/v1/books');

async function getBooks(): Promise<Array<BookPublic>> {
	if (typeof window === 'undefined') {
		return [];
	}

	const response = await fetch('/api/v1/books');
	// Watch : If a object as a null value, could cause problem with crud CallbackStateProvider
	let items = <Array<BookPublic>> await response.json()

	return items;
	// return items.map((value, index, array): Book2 => (
	// 	{
	// 		id: value.id,
	// 		title: value.title,
	// 		abstract: value.abstract,
	// 		author: value.author,
	// 		publisher: value.publisher,
	// 		isbn: value.isbn,
	// 		publication_date: value.publication_date,
	// 		language: value.language,
	// 		format: value.format,
	// 		cover: value.cover,
	// 		archived: value.archived,
	// 		created_date: value.created_date,
	// 		last_update_date: value.last_update_date,
	// 	}));
}

async function getoneBooks(book_id): Promise<BookPublic> {
	if (typeof window === 'undefined') {
		return <BookPublic>{};
	}

	const response = await fetch('/api/v1/books/'+book_id);
	// Watch : If a object as a null value, could cause problem with crud CallbackStateProvider
	return await response.json()
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
export const bookCrud2 = new CrudDefinition<BookPublic>({
	name: 'books2',
	label: { singular: 'Book', plural: 'Books' },
	 minStateLoadingTimeMs: 100,

	operations: [
		new List(
			[...fields],
			[
				new UrlAction('Edit', '/admin/books2/edit', Pen),
				new UrlAction('Delete', '/admin/books2/delete', TrashCan)
			],
			{
				globalActions: [
					new UrlAction('Quick Add', '/admin/newbook', Flash,  {buttonKind: 'danger-tertiary'}),
					new UrlAction('New', '/admin/books2/new', Pen),
				],
				}
		),
		new View([...fields]),
		new New(fields),
		new Edit(fields, []),
		new Delete(fields, new UrlAction('List', '/admin/books2/list'))
	],

	stateProcessor: new CallbackStateProcessor(function (
		data,
		operation,
		requestParameters: RequestParameters = {}
	) {
		if (operation.name === 'delete') {
			// alert('Hey, this delete is called with Javascript!');
			const id = (requestParameters.id || '').toString();
			bookApi.remove(id);

			return Promise.resolve();
		}

		if (operation.name === 'edit'){
			const entity = data as BookPublic;
			entity.id = (requestParameters.id || '').toString();
			bookApi.update(entity);
			Object.defineProperty(document, "referrer", {get : function(){ return "/admin/books2/list"; }});

			return Promise.resolve();
		}


		if (operation.name === 'new') {
				const entity = data as BookPublic;
				bookApi.add(entity);
				Object.defineProperty(document, "referrer", {get : function(){ return "/admin/books2/list"; }});

				return Promise.resolve();
		}

		console.error('StateProcessor error: Unsupported Books Crud action "' + operation.name + '".');

		return Promise.resolve();
	}),

	stateProvider: new CallbackStateProvider<BookPublic>(async function (
		operation,
		requestParameters: RequestParameters = {}
	) {
		console.info('Books provider called', { operation: operation.name, requestParameters });

		if (operation.name === 'list') {
			const page = parseInt((requestParameters.page || '1').toString());
			if (isNaN(page)) {
				throw new Error(`Invalid "page" value: expected a number, got "${page}".`);
			}

			let entities = await bookApi.list(0, 10);

			console.info('Entities: %o', entities);

			// Reduce abstact lenght
			entities.forEach((book) => {
				// book.cover = book.cover || "null"
				Object.keys(book).forEach(function(key) {
					if(book[key] === null) {
						book[key] = '-';
					}
				})
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

		if (operation.name === 'edit' || operation.name === 'view') {
			return bookApi.get((requestParameters?.id || '').toString());
			// return Promise.resolve(getStorage().get((requestParameters?.id || '').toString()));
		}

		if (operation.name === 'entity_view') {
			return bookApi.get((requestParameters?.field_value || '').toString());
			// return Promise.resolve(getStorage().get((requestParameters?.field_value || '').toString()));
		}

		// if (operation.name === 'entity_list') {
		// 	return bookApi.list(0, 100);
		// 	// return Promise.resolve(getStorage().all());
		// }

		console.error('StateProvider error: Unsupported Books Crud action "' + operation.name + '".');

		return Promise.resolve(null);
	})
});
