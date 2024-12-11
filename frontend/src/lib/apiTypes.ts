/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface BookBase {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	title: string;
	author: string;
	abstract?: string | null;
	publisher?: string | null;
	catalog?: string | null;
	category_type?: string | null;
	category_age?: string | null;
	category_topics?: string | null;
	language?: string | null;
	cover?: string | null;
	available?: boolean;
	isbn?: number | null;
	format?: string | null;
	publication_date?: string | null;
}
export interface BookCreate {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	title: string;
	author: string;
	abstract?: string | null;
	publisher?: string | null;
	catalog?: string | null;
	category_type?: string | null;
	category_age?: string | null;
	category_topics?: string | null;
	language?: string | null;
	cover?: string | null;
	available?: boolean;
	isbn?: number | null;
	format?: string | null;
	publication_date?: string | null;
}
export interface BookPublic {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	title: string;
	author: string;
	abstract?: string | null;
	publisher?: string | null;
	catalog?: string | null;
	category_type?: string | null;
	category_age?: string | null;
	category_topics?: string | null;
	language?: string | null;
	cover?: string | null;
	available?: boolean;
	isbn?: number | null;
	format?: string | null;
	publication_date?: string | null;
	id: number;
}
export interface BookTable {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	title: string;
	author: string;
	abstract?: string | null;
	publisher?: string | null;
	catalog?: string | null;
	category_type?: string | null;
	category_age?: string | null;
	category_topics?: string | null;
	language?: string | null;
	cover?: string | null;
	available?: boolean;
	isbn?: number | null;
	format?: string | null;
	publication_date?: string | null;
	id?: number | null;
}
export interface BookUpdate {
	archived?: boolean | null;
	created_date?: string | null;
	last_update_date?: string | null;
	title?: string | null;
	author?: string | null;
	abstract?: string | null;
	publisher?: string | null;
	catalog?: string | null;
	category_type?: string | null;
	category_age?: string | null;
	category_topics?: string | null;
	language?: string | null;
	cover?: string | null;
	available?: boolean | null;
	isbn?: number | null;
	format?: string | null;
	publication_date?: string | null;
}
export interface CirculationBase {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	borrowed_date: string;
	returned_date?: string | null;
	book_id?: number;
	member_id?: number;
}
export interface CirculationCreate {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	borrowed_date: string;
	returned_date?: string | null;
	book_id?: number;
	member_id?: number;
}
export interface CirculationPublic {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	borrowed_date: string;
	returned_date?: string | null;
	book_id?: number;
	member_id?: number;
	id: number;
}
export interface CirculationPublicWithRelationship {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	borrowed_date: string;
	returned_date?: string | null;
	book_id?: number;
	member_id?: number;
	id: number;
	book?: BookPublic | null;
	member?: MemberPublic | null;
}
export interface MemberPublic {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	family_referent?: boolean;
	firstname: string;
	surname: string;
	birthdate?: string | null;
	family_id?: number | null;
	id: number;
}
export interface CirculationTable {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	borrowed_date: string;
	returned_date?: string | null;
	book_id?: number;
	member_id?: number;
	id?: number | null;
}
export interface CirculationUpdate {
	archived?: boolean | null;
	created_date?: string | null;
	last_update_date?: string | null;
	borrowed_date?: string | null;
	returned_date?: string | null;
	book_id?: number | null;
	member_id?: number | null;
}
export interface FamilyBase {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	email: string | null;
	phone_number: string | null;
}
export interface FamilyCreate {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	email: string | null;
	phone_number: string | null;
}
export interface FamilyPublic {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	email: string | null;
	phone_number: string | null;
	id: number;
}
export interface FamilyPublicWithMembers {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	email: string | null;
	phone_number: string | null;
	id: number;
	members?: MemberPublic[];
}
export interface FamilyTable {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	email: string | null;
	phone_number: string | null;
	id?: number | null;
}
export interface FamilyUpdate {
	archived?: boolean | null;
	created_date?: string | null;
	last_update_date?: string | null;
	email?: string | null;
	phone_number?: string | null;
}
export interface MemberBase {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	family_referent?: boolean;
	firstname: string;
	surname: string;
	birthdate?: string | null;
	family_id?: number | null;
}
export interface MemberCreate {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	family_referent?: boolean;
	firstname: string;
	surname: string;
	birthdate?: string | null;
	family_id?: number | null;
}
export interface MemberPublicWithFamily {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	family_referent?: boolean;
	firstname: string;
	surname: string;
	birthdate?: string | null;
	family_id?: number | null;
	id: number;
	family?: FamilyPublic | null;
}
export interface MemberTable {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
	family_referent?: boolean;
	firstname: string;
	surname: string;
	birthdate?: string | null;
	family_id?: number | null;
	id?: number | null;
}
export interface MemberUpdate {
	archived?: boolean | null;
	created_date?: string | null;
	last_update_date?: string | null;
	family_referent?: boolean | null;
	firstname?: string | null;
	surname?: string | null;
	birthdate?: string | null;
	family_id?: number | null;
}
export interface SQLModel {}
export interface SharedBase {
	archived?: boolean;
	created_date?: string | null;
	last_update_date?: string | null;
}
export interface SharedUpdate {
	archived?: boolean | null;
	created_date?: string | null;
	last_update_date?: string | null;
}
export interface UserCreate {
	email: string;
	password: string;
	is_active?: boolean | null;
	is_superuser?: boolean | null;
	is_verified?: boolean | null;
}
export interface UserRead {
	id: string;
	email: string;
	is_active?: boolean;
	is_superuser?: boolean;
	is_verified?: boolean;
}
export interface UserUpdate {
	password?: string | null;
	email?: string | null;
	is_active?: boolean | null;
	is_superuser?: boolean | null;
	is_verified?: boolean | null;
}
