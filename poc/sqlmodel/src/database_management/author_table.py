from datetime import datetime, date

from sqlmodel import Session, select

from src.database_management.tables_definition import Author, EMPTY_STRING
from src.database_management.leafy_database import LeafyDatabase
from src.tools.log_management import LogManagement


class AuthorTable:
    """
    A class used to manage the author
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

    def create_author(
        self,
        name: str,
        description: str = EMPTY_STRING,
    ) -> Author:
        """Create an author reference

        Parameters
        ----------
        name
        description

        Returns
        ----------
        author reference
        """
        author = Author(
            name=name,
            description=description,
        )
        with Session(self._db_engine) as session:
            session.add(author)
            session.commit()
            session.refresh(author)
        self._log_ref.get_logger().info(f"add author: {author}")
        return author
