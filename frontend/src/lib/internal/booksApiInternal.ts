import type { BookPublic } from '../apiTypes';
import { InApiStorage } from './apiStorage';

let storage: null | InApiStorage<BookPublic> = null;


export function getStorage(): InApiStorage<BookPublic> {
	if (!storage) {
		console.log("new storage");
		storage = new InApiStorage<BookPublic>('/api/v1/books');
	}

	return storage;
}

