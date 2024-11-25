from datetime import datetime, date
import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.models import (
    AuthorTable,
    AuthorCreate,
    AuthorUpdate,
    AuthorSearch,
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
    Table reference
    """
    # setup
    verbosity = 2
    log_ref = LogManagement(verbosity, os.path.basename(__file__))
    db_mgmt = LeafyDatabase(log_ref)
    db_mgmt.start_database_engine()
    table_ref = TableManagement(log_ref, db_mgmt)

    # provide the data to the test
    yield table_ref

    # teardown
    db_mgmt.delete_database_permanentely()


def test_table_author_book_link(default_setup_teardown) -> None:
    table_ref: TableManagement = default_setup_teardown
    assert table_ref is not None

    # author_1: AuthorTable = table_ref.create_data(data=AuthorCreate(name="title"))
    author_2: AuthorTable = table_ref.create_data(
        data=AuthorCreate(name="newtitle", description="author")
    )
    # author_3: AuthorTable = table_ref.create_data(
    #     data=AuthorCreate(name="other", description="author")
    # )
    # author_4: AuthorTable = table_ref.create_data(
    #     data=AuthorCreate(name="name", description="otherdescription")
    # )
    book_1: BookTable = table_ref.create_data(
        data=BookCreate(
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
    )
    # book_2: BookTable = table_ref.create_data(
    #     data=BookCreate(
    #         title="new",
    #         author="other",
    #         synopsis="synopsis",
    #         edition="edition",
    #         catalog="catalog",
    #         category_type="category_type",
    #         category_age="category_age",
    #         category_topics="category_topics",
    #         langage="langage",
    #         cover="cover",
    #         available=True,
    #         archived=True,
    #     )
    # )
    # book_3: BookTable = table_ref.create_data(
    #     data=BookCreate(title="new", author="author2")
    # )
    # book_4: BookTable = table_ref.create_data(
    #     data=BookCreate(title="test", author="test", available=False, archived=False)
    # )

    book_link, author_link = table_ref.make_link(book_1, author_2)
    print(f"book_1: {book_1}")
    print(f"author_2: {author_2}")
    print(f"book_link: {book_link}")
    print(f"author_link: {author_link}")

    test_book = table_ref.get_data(book_link.id, BookTable)
    print(f"test_book: {test_book}")
    print(f"test_book: {test_book.authors}")
    # print(f"book_link authors: {book_link.authors}")
    # print(f"author_link books: {author_link.books}")

    # data_list = table_ref.get_data_list(AuthorSearch(name="title"))
    # assert len(data_list) == 2
    # assert author_1 in data_list
    # assert author_2 in data_list

    # data_list = table_ref.get_data_list(AuthorSearch(description="author"))
    # assert len(data_list) == 2
    # assert author_2 in data_list
    # assert author_3 in data_list

    # data_list = table_ref.get_data_list(AuthorSearch())
    # assert len(data_list) == 4
    # assert author_1 in data_list
    # assert author_2 in data_list
    # assert author_3 in data_list
    # assert author_4 in data_list
