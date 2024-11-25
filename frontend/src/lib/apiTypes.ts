/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface Book {
  title: string;
  author: string;
  publisher: string;
  isbn13: number;
  publication_year: number | string;
  abstract: string;
  language: string;
  format: string;
  url?: string | "" | null;
}
