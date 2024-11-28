import logging
import os

from sqlmodel import SQLModel, create_engine

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

        connect_args = {"check_same_thread": False}  # to work with FastAPI
        self._engine = create_engine(
            sqlite_url, echo=engine_echo, connect_args=connect_args
        )

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
