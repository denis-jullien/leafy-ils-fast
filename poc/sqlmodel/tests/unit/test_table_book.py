from datetime import datetime, date
import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.models import (
    BookTable,
    BookCreate,
    BookTable,
    BookCreate,
    BookUpdate,
    BookSearch,
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
    BookTable reference
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
    [
        BookCreate(title="title", author="author"),
        BookCreate(
            title="title",
            author="author",
            synopsis="synopsis",
            edition="edition",
            catalog="catalog",
            category_type="category_type",
            category_age="category_age",
            category_topics="category_topics",
            langage="langage",
            cover="cover",
            available=False,
            archived=True,
            registration_date=date.fromisoformat("2019-12-04"),
        ),
    ],
)
def test_create_book(default_setup_teardown, data) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    my_book: BookTable = table_ref.create_data(data=data)
    result, failure_message = does_model_contain_submodel(my_book, data)
    assert result, failure_message


def test_get_book(default_setup_teardown) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    book_1_data = BookCreate(
        title="title",
        author="author",
        synopsis="synopsis",
        edition="edition",
        catalog="catalog",
        category_type="category_type",
        category_age="category_age",
        category_topics="category_topics",
        langage="langage",
        cover="cover",
        available=True,
        archived=False,
    )
    book_2_data = BookCreate(
        title="new",
        author="other",
        synopsis="synopsis",
        edition="edition",
        catalog="catalog",
        category_type="category_type",
        category_age="category_age",
        category_topics="category_topics",
        langage="langage",
        cover="cover",
        available=True,
        archived=True,
    )
    book_3_data = BookCreate(title="new", author="author2")
    book_4_data = BookCreate(
        title="test", author="test", available=False, archived=False
    )

    book_1: BookTable = table_ref.create_data(data=book_1_data)
    book_2: BookTable = table_ref.create_data(data=book_2_data)
    book_3: BookTable = table_ref.create_data(data=book_3_data)
    book_4: BookTable = table_ref.create_data(data=book_4_data)
    book_list = table_ref.get_data_list(BookSearch(title="title"))
    assert len(book_list) == 1
    assert book_1 in book_list

    book_list = table_ref.get_data_list(BookSearch(author="author"))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_3 in book_list

    book_list = table_ref.get_data_list(BookSearch(synopsis="synopsis"))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(edition="edition"))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(catalog="catalog"))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(category_type="category_type"))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(category_age="category_age"))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(category_topics="category_topics"))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(langage="langage"))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(cover=""))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(available=True))
    assert len(book_list) == 3
    assert book_1 in book_list
    assert book_2 in book_list
    assert book_3 in book_list

    book_list = table_ref.get_data_list(BookSearch(archived=True))
    assert len(book_list) == 1
    assert book_2 in book_list

    book_list = table_ref.get_data_list(BookSearch(available=True, archived=False))
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_3 in book_list

    book_list = table_ref.get_data_list(BookSearch())
    assert len(book_list) == 4
    assert book_1 in book_list
    assert book_2 in book_list
    assert book_3 in book_list
    assert book_4 in book_list


@pytest.mark.parametrize(
    "init_data",
    [
        BookCreate(title="title", author="author"),
        BookCreate(
            title="title",
            author="author",
            synopsis="synopsis",
            edition="edition",
            catalog="catalog",
            category_type="category_type",
            category_age="category_age",
            category_topics="category_topics",
            langage="langage",
            cover="cover",
            available=False,
            archived=True,
            registration_date=date.fromisoformat("2019-12-04"),
        ),
    ],
)
@pytest.mark.parametrize(
    "new_data",
    [
        BookUpdate(title="new"),
        BookUpdate(
            title="newtitle",
            author="newauthor",
            synopsis="newsynopsis",
            edition="newedition",
            catalog="newcatalog",
            category_type="newcategory_type",
            category_age="newcategory_age",
            category_topics="newcategory_topics",
            langage="newlangage",
            cover="newcover",
            available=True,
            archived=False,
            registration_date=date.fromisoformat("1993-12-04"),
        ),
        BookUpdate(),
    ],
)
def test_update_book(default_setup_teardown, init_data, new_data) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    my_book: BookTable = table_ref.create_data(data=init_data)
    my_book: BookTable = table_ref.update_data(my_book, new_data)
    result, failure_message = does_model_contain_submodel_updated(
        my_book, init_data, new_data
    )
    assert result, failure_message


def test_delete_table_book(default_setup_teardown) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    data = BookCreate(
        title="title",
        author="author",
        synopsis="synopsis",
        edition="edition",
        catalog="catalog",
        category_type="category_type",
        category_age="category_age",
        category_topics="category_topics",
        langage="langage",
        cover="cover",
        available=False,
        archived=True,
        registration_date=date.fromisoformat("2019-12-04"),
    )

    my_book: BookTable = table_ref.create_data(data=data)

    data_list = table_ref.get_data_list(BookSearch())
    assert len(data_list) == 1

    table_ref.delete_data(my_book)
    assert True

    data_list = table_ref.get_data_list(BookSearch())
    assert len(data_list) == 0
