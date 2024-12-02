import type { BookPublic } from '../apiTypes';
import { MyApiInterface } from './apiStorage';

let storage: null | MyApiInterface<BookPublic> = null;


export function getStorage(): MyApiInterface<BookPublic> {
	if (!storage) {
		console.log("new storage");
		storage = new MyApiInterface<BookPublic>('/api/v1/books');
	}

	return storage;
}

