import argparse
import datetime
import logging
import pytest

from sqlmodel import Session, select

from database_definition import Book, Catalog, CategoryType, CategoryAge, CategoryTopic, BorrowHistory
from leafy_database import LeafyDatabase
from log_management import LogManagement


class CatalogManagement:
    """
    A class used to manage the books' catalog
    """

    EMPTY_DATA = ""

    def __init__(self, log_ref: LogManagement, db: LeafyDatabase) -> None:
        """Initialize the class to manage the Book database's tables

        Parameters
        ----------
        log_ref: log management reference
        db: database reference
        """
        self._log_ref = log_ref
        self._db = db
        self._db_engine = self._db.get_database_engine()

    def get_book_list(
        self, title: str | None = None, author: str | None = None
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
            search_mapping = [(title, Book.title), (author, Book.author)]
            statement = self._db.search_table_elements(statement, search_mapping)

            results = session.exec(statement)
            book_list = results.all()
        return book_list

    def create_book(
        self,
        title: str,
        author: str,
        synopsis: str = EMPTY_DATA,
        edition: str = EMPTY_DATA,
    ) -> Book:
        """Create a new book reference

        Parameters
        ----------
        title
        author
        ...

        Returns
        ----------
        book reference
        """
        registration_date = datetime.datetime.today()
        book = Book(
            unique_id="",
            title=title,
            author=author,
            synopsis=synopsis,
            edition=edition,
            category_type=CategoryType.NOVEL,
            category_age=CategoryAge.SENIOR,
            catalog=Catalog.US,
            registration_date=registration_date,
            last_update_date=registration_date,
        )
        with Session(self._db_engine) as session:
            session.add(book)
            session.commit()
            session.refresh(book)
        self._log_ref.get_logger().info(f"add a new book: {book}")
        return book

    def update_book(
        self,
        book: Book,
        title: str | None = None,
        author: str | None = None,
        synopsis: str | None = None,
        edition: str | None = None,
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

        book.last_update_date = datetime.datetime.today()

        with Session(self._db_engine) as session:
            session.add(book)
            session.commit()
            session.refresh(book)
        self._log_ref.get_logger().info(f"update a book: {book}")
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
        self._log_ref.get_logger().info(f"delete a book: {book}")
        return book

    def get_borrow_history_list(
        self, book: Book | None = None, release_date: datetime.date | None = None, return_date: datetime.date | None = None
    ) -> list[BorrowHistory]:
        """Get list of history's references

        Parameters
        ----------
        book: if not None, search for history by book
        release_date: if not None, search for history by release_date
        return_date: if not None, search for history by return_date

        Returns
        ----------
        list of history's references depending of the parameters
        """
        with Session(self._db_engine) as session:
            # Get all base
            statement = select(BorrowHistory)

            # mapping of value to look for with column names
            search_mapping = [(release_date, Book.release_date), (return_date, Book.return_date)]
            if book is not None:
                search_mapping.append((book.id, BorrowHistory.book_id))
            statement = self._db.search_table_elements(statement, search_mapping)

            results = session.exec(statement)
            history_list = results.all()
        return history_list

    def create_borrow_history(
        self,
        book: Book,
        release_date: datetime.date | None = None,
        return_date: datetime.date | None = None,
    ) -> BorrowHistory:
        """Create a new history reference

        Parameters
        ----------
        book
        release_date
        return_date
        ...

        Returns
        ----------
        history reference
        """
        if release_date is None:
            release_date = datetime.datetime.today()
        history = BorrowHistory(
            book=book,
            release_date=release_date,
            return_date=return_date,
        )
        with Session(self._db_engine) as session:
            session.add(history)
            session.commit()
            session.refresh(history)
            session.refresh(book)
        self._log_ref.get_logger().info(f"add a new history: {history}")
        return history

    def update_borrow_history(
        self,
        history: BorrowHistory,
        book: Book | None = None,
        release_date: datetime.date | None = None,
        return_date: datetime.date | None = None,
    ) -> BorrowHistory:
        """Update borrow history

        Parameters
        ----------
        history
        book
        release_date
        return_date

        Returns
        ----------
        history reference
        """
        if book is not None:
            history.book = book
        if release_date is not None:
            history.release_date = release_date
        if return_date is not None:
            history.return_date = return_date

        with Session(self._db_engine) as session:
            session.add(history)
            session.commit()
            session.refresh(history)
            if book is not None:
                session.refresh(book)
        self._log_ref.get_logger().info(f"update history: {history}")
        return history

    def delete_borrow_history(self, history: BorrowHistory) -> None:
        """Delete a borrow history

        Parameters
        ----------
        history
        """
        with Session(self._db_engine) as session:
            book = history.book
            session.delete(history)
            session.commit()
            if book is not None:
                session.refresh(book)
        self._log_ref.get_logger().info(f"delete history: {history}")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="""
        """
    )
    argparser.add_argument(
        "-v", "--verbosity", action="count", help="increase output verbosity"
    )
    args = argparser.parse_args()

    log_ref = LogManagement(args.verbosity, "test")

    leafy_database = LeafyDatabase(log_ref)
    leafy_database.start_database_engine()
    database_engine = leafy_database.get_database_engine()

    # Tests
    catalog_mgmt = CatalogManagement(log_ref, leafy_database)

    book_1 = catalog_mgmt.create_book("my_title", "my_author")
    book_1 = catalog_mgmt.update_book(book_1, "my new title", "my_new_author")
    book_2 = catalog_mgmt.create_book(
        "my_title2", "my_author2", synopsis="test", edition="test2"
    )
    book_3 = catalog_mgmt.create_book(
        "my_title3", "my_author3", synopsis="test", edition="test3"
    )
    catalog_mgmt.delete_book(book_3)

    log_ref.get_logger().info(f"\n\nget_book_list: \n")
    book_list = catalog_mgmt.get_book_list(title="my_title2")
    log_ref.get_logger().info(f"book_list: {book_list}")
    book_list = catalog_mgmt.get_book_list(title="Title ")
    log_ref.get_logger().info(f"book_list: {book_list}")
    book_list = catalog_mgmt.get_book_list(title="other")
    log_ref.get_logger().info(f"book_list: {book_list}")
    book_list = catalog_mgmt.get_book_list(author="my_author")
    log_ref.get_logger().info(f"book_list: {book_list}")
    book_list = catalog_mgmt.get_book_list(title="title", author="new")
    log_ref.get_logger().info(f"book_list: {book_list}")

    # Print table from database
    log_level = log_ref.get_logging_level()
    if log_level == logging.INFO or log_level == logging.DEBUG:
        with Session(database_engine) as session:
            for cl in [Book]:
                log_ref.get_logger().info(f"\n\n{cl}: \n")
                statement = select(cl)
                results = session.exec(statement)
                for elem in results:
                    log_ref.get_logger().info(f"{elem}")

    # TODO: remove later
    leafy_database.delete_database_permanentely()
