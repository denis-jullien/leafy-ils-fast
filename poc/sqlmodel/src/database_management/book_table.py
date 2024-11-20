from datetime import datetime, date

from sqlmodel import Session, select

from src.database_management.tables_definition import Book, EMPTY_STRING
from src.database_management.leafy_database import LeafyDatabase
from src.tools.log_management import LogManagement


class BookTable:
    """
    A class used to manage the books' catalog
    """

    def __init__(self, log_ref: LogManagement, db: LeafyDatabase) -> None:
        """Initialize the class

        Parameters
        ----------
        log_ref: log management reference
        db: database reference
        """
        self._log_ref = log_ref
        self._db = db
        self._db_engine = self._db.get_database_engine()

    def create_book(
        self,
        title: str,
        author: str,
        synopsis: str = EMPTY_STRING,
        edition: str = EMPTY_STRING,
        catalog: str = EMPTY_STRING,
        category_type: str = EMPTY_STRING,
        category_age: str = EMPTY_STRING,
        category_topics: str = EMPTY_STRING,
        langage: str = EMPTY_STRING,
        cover: str = None,
        available: bool = True,
        archived: bool = False,
        registration_date: date | None = None,
    ) -> Book:
        """Create a new book reference

        Parameters
        ----------
        title
        author
        ...
        registration_date: if None, the release_date will be today

        Returns
        ----------
        book reference
        """
        if registration_date is None:
            registration_date = datetime.today()
            last_update_date = registration_date
        else:
            last_update_date = datetime.today()
        book = Book(
            title=title,
            author=author,
            synopsis=synopsis,
            edition=edition,
            catalog=catalog,
            category_type=category_type,
            category_age=category_age,
            category_topics=category_topics,
            langage=langage,
            cover=cover,
            available=available,
            archived=archived,
            registration_date=registration_date,
            last_update_date=last_update_date,
        )
        with Session(self._db_engine) as session:
            session.add(book)
            session.commit()
            session.refresh(book)
        self._log_ref.get_logger().info(f"add book: {book}")
        return book

    def get_book_list(
        self,
        title: str | None = None,
        author: str | None = None,
        synopsis: str | None = None,
        edition: str | None = None,
        catalog: str | None = None,
        category_type: str | None = None,
        category_age: str | None = None,
        category_topics: str | None = None,
        langage: str | None = None,
        cover: str | None = None,
        available: bool | None = None,
        archived: bool | None = None,
    ) -> list[Book]:
        """Get list of book's references

        Parameters
        ----------
        title: if not None, search for book by title
        author: if not None, search for book by author

        Returns
        ----------
        list of book's references depending of the parameters
        """
        with Session(self._db_engine) as session:
            # Get all base
            statement = select(Book)

            # mapping of value to look for with column names
            search_mapping = [
                (title, Book.title),
                (author, Book.author),
                (author, Book.author),
                (synopsis, Book.synopsis),
                (edition, Book.edition),
                (catalog, Book.catalog),
                (category_type, Book.category_type),
                (category_age, Book.category_age),
                (category_topics, Book.category_topics),
                (langage, Book.langage),
                (cover, Book.cover),
                (available, Book.available),
                (archived, Book.archived),
            ]
            statement = self._db.search_table_elements(statement, search_mapping)

            results = session.exec(statement)
            book_list = results.all()
        return book_list

    def update_book(
        self,
        book: Book,
        title: str | None = None,
        author: str | None = None,
        synopsis: str | None = None,
        edition: str | None = None,
        catalog: str | None = None,
        category_type: str | None = None,
        category_age: str | None = None,
        category_topics: str | None = None,
        langage: str | None = None,
        cover: str | None = None,
        available: bool | None = None,
        archived: bool | None = None,
    ) -> Book:
        """Update a book

        Parameters
        ----------
        book: book reference
        title
        author
        ...

        Returns
        ----------
        book reference
        """
        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if synopsis is not None:
            book.synopsis = synopsis
        if edition is not None:
            book.edition = edition
        if catalog is not None:
            book.catalog = catalog
        if category_type is not None:
            book.category_type = category_type
        if category_age is not None:
            book.category_age = category_age
        if category_topics is not None:
            book.category_topics = category_topics
        if langage is not None:
            book.langage = langage
        if cover is not None:
            book.cover = cover
        if available is not None:
            book.available = available
        if archived is not None:
            book.archived = archived

        book.last_update_date = datetime.today()

        with Session(self._db_engine) as session:
            session.add(book)
            session.commit()
            session.refresh(book)
        self._log_ref.get_logger().info(f"update book: {book}")
        return book

    def delete_book(self, book: Book) -> None:
        """Delete a book

        Parameters
        ----------
        book: book reference
        """
        with Session(self._db_engine) as session:
            session.delete(book)
            session.commit()
        self._log_ref.get_logger().info(f"delete book: {book}")
        return book
