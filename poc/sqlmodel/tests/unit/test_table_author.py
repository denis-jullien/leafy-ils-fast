from datetime import datetime, date
import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.models import (
    AuthorTable,
    AuthorCreate,
    AuthorUpdate,
    AuthorSearch,
)
from src.database_management.leafy_database import LeafyDatabase
from src.database_management.table_management import TableManagement
from src.tools.tools_for_tests import (
    does_model_contain_submodel,
    does_model_contain_submodel_updated,
)


@pytest.fixture
def default_setup_teardown():
    """
    default setup / teardown

    Yield
    ----------
    Table reference
    """
    # setup
    verbosity = None
    log_ref = LogManagement(verbosity, os.path.basename(__file__))
    db_mgmt = LeafyDatabase(log_ref)
    db_mgmt.start_database_engine()
    table_ref = TableManagement(log_ref, db_mgmt)

    # provide the data to the test
    yield table_ref

    # teardown
    db_mgmt.delete_database_permanentely()


@pytest.mark.parametrize(
    "data",
    [AuthorCreate(name="title"), AuthorCreate(name="title", description="author")],
)
def test_create_table_author(default_setup_teardown, data) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    my_author: AuthorTable = table_ref.create_data(data=data)
    result, failure_message = does_model_contain_submodel(my_author, data)
    assert result, failure_message


def test_get_table_author(default_setup_teardown) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    author_1: AuthorTable = table_ref.create_data(data=AuthorCreate(name="title"))
    author_2: AuthorTable = table_ref.create_data(
        data=AuthorCreate(name="newtitle", description="author")
    )
    author_3: AuthorTable = table_ref.create_data(
        data=AuthorCreate(name="other", description="author")
    )
    author_4: AuthorTable = table_ref.create_data(
        data=AuthorCreate(name="name", description="otherdescription")
    )

    data_list = table_ref.get_data_list(AuthorSearch(name="title"))
    assert len(data_list) == 2
    assert author_1 in data_list
    assert author_2 in data_list

    data_list = table_ref.get_data_list(AuthorSearch(description="author"))
    assert len(data_list) == 2
    assert author_2 in data_list
    assert author_3 in data_list

    data_list = table_ref.get_data_list(AuthorSearch())
    assert len(data_list) == 4
    assert author_1 in data_list
    assert author_2 in data_list
    assert author_3 in data_list
    assert author_4 in data_list


@pytest.mark.parametrize(
    "init_data",
    [AuthorCreate(name="title", description="author"), AuthorCreate(name="title")],
)
@pytest.mark.parametrize(
    "new_data",
    [
        AuthorUpdate(name="title"),
        AuthorUpdate(name="title", description="author"),
        AuthorUpdate(),
    ],
)
def test_update_table_author(default_setup_teardown, init_data, new_data) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    my_author: AuthorTable = table_ref.create_data(data=init_data)

    my_author: AuthorTable = table_ref.update_data(my_author, new_data)
    result, failure_message = does_model_contain_submodel_updated(
        my_author, init_data, new_data
    )
    assert result, failure_message


def test_delete_table_author(default_setup_teardown) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    data = AuthorCreate(name="title", description="author")

    my_author: AuthorTable = table_ref.create_data(data=data)

    data_list = table_ref.get_data_list(AuthorSearch())
    assert len(data_list) == 1

    table_ref.delete_data(my_author)
    assert True

    data_list = table_ref.get_data_list(AuthorSearch())
    assert len(data_list) == 0
