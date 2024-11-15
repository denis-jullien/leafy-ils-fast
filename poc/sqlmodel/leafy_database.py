import logging
import os
import pytest

from sqlmodel import SQLModel, create_engine
from sqlalchemy.sql import func

from log_management import LogManagement


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


# Unit tests

# Currently, doesn't worked


@pytest.fixture
def default_setup():
    """
    default setup / teardown
    debug: bool = False, db_name: str = None
    """

    def _default_setup(debug: bool = False, db_name: str | None = None):
        # setup
        if debug == True:
            verbosity = 4
        else:
            verbosity = None
        log_ref = LogManagement(verbosity, os.path.basename(__file__))

        if db_name == None:
            db_mgmt = LeafyDatabase(log_ref)
            db_name = LeafyDatabase.DEFAULT_DATABASE_NAME
        else:
            db_mgmt = LeafyDatabase(log_ref, database_name=db_name)

        # provide the data to the test
        yield db_mgmt

        # teardown
        if os.path.isfile(db_name):
            os.remove(db_name)

    return _default_setup


@pytest.mark.parametrize("debug", [False, True])
def test_init(debug, default_setup) -> None:
    print(f"ici")
    db_mgmt = default_setup(debug, None)
    print(f"db_mgmt: {db_mgmt}")
    assert db_mgmt != None


# class TestLeafyDatabase:
#     """
#     TODO: find a clean way for setup/teardown
#     """
#     # log_ref = LogManagement(0, "test_not_debug")
#     # log_ref_debug = LogManagement(4, "test_debug")

#     # @pytest.fixture
#     def default_setup(self, debug: bool = False, db_name: str = None) -> list[LeafyDatabase, str]:
#         """
#         prepare
#         """
#         # setup
#         if debug == True:
#             verbosity = 4
#         else:
#             verbosity = None
#         log_ref = LogManagement(verbosity, "test_database")

#         if db_name == None:
#             db_mgmt = LeafyDatabase(log_ref)
#             db_name = LeafyDatabase.DEFAULT_DATABASE_NAME
#         else:
#             db_mgmt = LeafyDatabase(log_ref, database_name=db_name)

#         # provide the data to the test
#         # yield db_mgmt, db_name
#         return db_mgmt, db_name

#     # @pytest.fixture
#     def default_teardown(self, db_name: str = None) -> None:
#         # teardown
#         if os.path.isfile(db_name):
#             os.remove(db_name)

#     def test_init_not_debug(self) -> None:
#         db_mgmt, _ = self.default_setup(debug = False)
#         assert db_mgmt != None

#     def test_init_debug(self) -> None:
#         db_mgmt, _ = self.default_setup(debug = True)
#         assert db_mgmt != None

#     def test_get_database_engine(self) -> None:
#         db_mgmt, _ = self.default_setup()
#         db_engine = db_mgmt.get_database_engine()
#         assert db_engine != None

#     @pytest.mark.parametrize("db_name", [None, "test.db"])
#     def test_start_database_engine(self, db_name: str | None) -> None:
#         db_mgmt, db_name = self.default_setup(db_name = db_name)

#         assert os.path.isfile(db_name) == False
#         db_mgmt.start_database_engine()
#         assert os.path.isfile(db_name) == True

#         self.default_teardown(db_name)

#     @pytest.mark.parametrize("db_name", [None, "test.db"])
#     def test_remove_database_engine(self, db_name: str | None) -> None:
#         db_mgmt, db_name = self.default_setup(db_name = db_name)
#         db_mgmt.start_database_engine()

#         assert os.path.isfile(db_name) == True
#         db_mgmt.delete_database_permanentely()
#         assert os.path.isfile(db_name) == False

#         self.default_teardown(db_name)
