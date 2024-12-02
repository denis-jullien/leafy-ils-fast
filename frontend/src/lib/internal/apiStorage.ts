type Entity = object & { id: string | number };

export interface InternalStorage<T extends Entity> {
	list(): Array<T>;
	get(id: string | number): T;
	add(object: T): void;
	remove(id: string | number): void;
	update(object: T): void;
}

export class InApiStorage<T extends Entity> implements InternalStorage<T> {
	public readonly objectBaseUrl: string;
	public readonly localStorageName: string;
	private items: Array<T> = [];

	constructor(objectName: string) {
		this.objectBaseUrl = objectName;

		this.localStorageName = 'svelte-admin-dev-' + this.objectBaseUrl.replace(/s$/g, '').toLowerCase();
	}

	public get(id: string | number): T {
		const found = this.all().filter((b) => b.id.toString() === id.toString());

		if (found.length === 0) {
			throw new Error(`Object of type "${this.objectBaseUrl}" with id "${id}" was not found.`);
		}

		if (found.length !== 1) {
			throw new Error(
				`Error: Found multiple objects of type "${this.objectBaseUrl}" with id "${id}".`
			);
		}

		return found[0];
	}

	public remove(id: string | number): void {
		const item = this.get(id);

		this.saveList(this.all().filter((b) => b.id.toString() !== item.id.toString()));
	}

	public add(object: T): void {
		let item: T | null = null;
		try {
			item = this.get(object.id);
		} catch (e) {
			console.error('Could not fetch item from storage: ');
			console.error(e);
		}
		if (item) {
			throw new Error(
				`Attempted to create new object of type "${this.objectBaseUrl}", but its ID was already found. Did you mean to use "update" instead?`
			);
		}

		this.saveList([...this.all(), object]);
	}

	public update(object: T): void {
		const item = this.get(object.id);

		this.saveList(this.all().map((i) => (i.id === item.id ? item : i)));
	}

	public all(): Array<T> {
		if (this.items.length) {
			return this.items;
		}
		if (typeof window === 'undefined') {
			return [];
		}

		let memory = window.localStorage.getItem(this.localStorageName);
		if (memory === null || memory === undefined || memory === '') {
			// memory = JSON.stringify(this.baseInitializer(), this.serializeReplacer);
			window.localStorage.setItem(this.localStorageName, memory);
		}

		this.items = JSON.parse(memory);

		return this.items;
	}

	private saveList(newList: T[]) {
		const serialized = JSON.stringify(newList, this.serializeReplacer);
		window.localStorage.setItem(this.localStorageName, serialized);
	}

	private serializeReplacer(this: T, key: string, value: unknown): unknown {
		if (key === '__crud_operation') {
			return undefined;
		}

		return value;
	}
}
