import logging
import os

from sqlmodel import SQLModel, create_engine
from sqlalchemy.sql import func

from tools.log_management import LogManagement


class LeafyDatabase:
    """
    A class used to manage the database at an high level
    """

    DEFAULT_DATABASE_NAME = "database.db"

    def __init__(
        self, log_ref: LogManagement, database_name: str = DEFAULT_DATABASE_NAME
    ) -> None:
        """Initialize database configuration

        Parameters
        ----------
        log_ref: log management reference
        """
        self._database_name = database_name
        self._log_ref = log_ref
        sqlite_url = f"sqlite:///{self._database_name}"

        if self._log_ref.get_logging_level() == logging.DEBUG:
            engine_echo = True
        else:
            engine_echo = False
        self._engine = create_engine(sqlite_url, echo=engine_echo)

    def start_database_engine(self):
        """Start database engine"""
        SQLModel.metadata.create_all(self._engine)

    def get_database_engine(self):
        """Get database engine reference

        Returns
        ----------
        database engine reference
        """
        return self._engine

    def delete_database_permanentely(self):
        """Delete database file"""
        os.remove(self._database_name)

    def normalize_string(self, string):
        """normalize strings (case-insensitive, remove spaces and special characters)"""
        return func.replace(func.replace(func.lower(string), " ", ""), "-", "")

    def search_table_elements(self, statement, search_mapping: list):
        """Search elements' table in a statement from a SQLModel select according to search_mapping

        Parameters
        ----------
        statement:
            result of SQLModel select
            ex: statement = select(Book)
        search_mapping
            dynamically add filters based on non-None arguments
            ex1:
                search_mapping = [
                    (title, Book.title),
                    (author, Book.author)
                ]
            ex2:
                search_mapping = [
                    (firstname, FamilyMember.firstname),
                    (surname, FamilyMember.surname),
                    (birthdate, FamilyMember.birthdate),
                    (family_referent, FamilyMember.family_referent),
                ]
                if family is not None:
                    search_mapping.append((family.id, FamilyMember.family_id))

        Returns
        ----------
        statement updated
        """
        for value, column in search_mapping:
            if value is not None:
                statement = statement.where(
                    self.normalize_string(column).contains(self.normalize_string(value))
                )
        return statement
