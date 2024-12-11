import type { InternalStorage } from '$lib/internal/memoryStorage';
import type { BookPublic } from '$lib/apiTypes';

type Entity = object & { id: string | number };

export interface InternalApiInterface<T extends Entity> {
	list(offset: number, limit: number): Promise<Array<T>>;
	get(id: string | number): Promise<T>;
	add(object: T): void;
	remove(id: string | number): void;
	update(object: T): void;
}

export class MyApiInterface<T extends Entity> implements InternalApiInterface<T> {
	public readonly objectBaseUrl: string;
	// private items: Array<T> = [];

	constructor(objectName: string) {
		this.objectBaseUrl = objectName;
	}

	public async get(id: string | number): Promise<T> {
		if (typeof window === 'undefined') {
			return Promise.resolve(<T>{});
		}

		// const found = this.all().filter((b) => b.id.toString() === id.toString());
		const response = await fetch(this.objectBaseUrl + '/' + id.toString());
		// Watch : If a object as a null value, could cause problem with crud CallbackStateProvider

		if (response.status !== 200) {
			throw new Error(`Object of type "${this.objectBaseUrl}" with id "${id}" was not found.`);
		}

		return response.json();
	}

	public remove(id: string | number): void {
		const item = this.get(id);

		// this.saveList(this.all().filter((b) => b.id.toString() !== item.id.toString()));
	}

	public add(object: T): void {
		// let item: T | null = null;
		// try {
		// 	item = this.get(object.id);
		// } catch (e) {
		// 	console.error('Could not fetch item from storage: ');
		// 	console.error(e);
		// }
		// if (item) {
		// 	throw new Error(
		// 		`Attempted to create new object of type "${this.objectBaseUrl}", but its ID was already found. Did you mean to use "update" instead?`
		// 	);
		// }
		//
		// this.saveList([...this.all(), object]);
		alert('add');
	}

	public update(object: T): void {
		const item = this.get(object.id);
		// alert("upodatez")
		// this.saveList(this.all().map((i) => (i.id === item.id ? item : i)));
	}

	public async list(offset: number, limit: number): Promise<Array<T>> {
		// if (this.items.length) {
		// 	return this.items;
		// }
		if (typeof window === 'undefined') {
			return [];
		}

		const response = await fetch('/api/v1/books');
		// Watch : If a object as a null value, could cause problem with crud CallbackStateProvider
		return response.json();
	}
}
