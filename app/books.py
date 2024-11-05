from pydantic import BaseModel, PositiveInt
from pydantic_extra_types.language_code import LanguageAlpha2

def clean_isbn(value):
    isbn, sep, remainder = value.strip().partition(' ')
    if len(isbn) < 10:
        return ''
    for char in '-:.;':
        isbn = isbn.replace(char, '')
    return isbn

class Book(BaseModel):
    title: str  
    author: str 
    publisher: str
    isbn13: PositiveInt
    publication_year: PositiveInt
    abstract: str
    language: LanguageAlpha2
    format: str