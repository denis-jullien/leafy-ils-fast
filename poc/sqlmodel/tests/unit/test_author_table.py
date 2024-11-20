from datetime import datetime, date
import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.tables_definition import Author, EMPTY_STRING
from src.database_management.leafy_database import LeafyDatabase
from src.database_management.author_table import AuthorTable


@pytest.fixture
def default_setup_teardown():
    """
    default setup / teardown

    Yield
    ----------
    AuthorTable reference
    """
    # setup
    verbosity = None
    log_ref = LogManagement(verbosity, os.path.basename(__file__))
    db_mgmt = LeafyDatabase(log_ref)
    db_mgmt.start_database_engine()
    author_ref = AuthorTable(log_ref, db_mgmt)

    # provide the data to the test
    yield author_ref

    # teardown
    db_mgmt.delete_database_permanentely()


@pytest.mark.parametrize(
    "name,description",
    [
        ("title", "author"),
        ("title", ""),
    ],
)
def test_create_author(default_setup_teardown, name, description) -> None:
    author_ref: AuthorTable = default_setup_teardown
    assert author_ref is not None

    my_author: Author = author_ref.create_author(
        name=name,
        description=description,
    )
    assert my_author.name == name
    assert my_author.description == description
