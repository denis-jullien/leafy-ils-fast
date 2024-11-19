from datetime import datetime, date

from sqlmodel import Session, select

from src.database_management.tables_definition import Book, BorrowHistory
from src.database_management.leafy_database import LeafyDatabase
from src.tools.log_management import LogManagement


class BorrowHistoryTable:
    """
    A class used to manage the borrow history table
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

    def create_borrow_history(
        self,
        book: Book,
        release_date: date | None = None,
        return_date: date | None = None,
    ) -> BorrowHistory:
        """Create borrow history

        Parameters
        ----------
            book: should have been created through BookTable
            release_date: if None, the release_date will be today
            return_date (optional)

        Returns
        ----------
            borrow history reference
        """
        if release_date is None:
            release_date = datetime.today()
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
        self._log_ref.get_logger().info(f"create borrow history: {history}")
        return history

    def get_borrow_history_list(
        self,
        book: Book | None = None,
        release_date: date | None = None,
        return_date: date | None = None,
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
            search_mapping = [
                (release_date, BorrowHistory.release_date),
                (return_date, BorrowHistory.return_date),
            ]
            if book is not None:
                search_mapping.append((book.id, BorrowHistory.book_id))
            statement = self._db.search_table_elements(statement, search_mapping)

            results = session.exec(statement)
            history_list = results.all()
        return history_list

    def update_borrow_history(
        self,
        history: BorrowHistory,
        book: Book | None = None,
        release_date: date | None = None,
        return_date: date | None = None,
    ) -> BorrowHistory:
        """Update borrow history

        Parameters
        ----------
            history: borrow history reference
            book
            release_date
            return_date

        Returns
        ----------
            borrow history reference
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
        self._log_ref.get_logger().info(f"update borrow history: {history}")
        return history

    def delete_borrow_history(self, history: BorrowHistory) -> None:
        """Delete a borrow history

        Parameters
        ----------
            borrow history reference
        """
        with Session(self._db_engine) as session:
            session.delete(history)
            session.commit()
        self._log_ref.get_logger().info(f"delete history: {history}")
