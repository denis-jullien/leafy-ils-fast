from datetime import datetime, date
import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.tables_definition import Book, BorrowHistory
from src.database_management.leafy_database import LeafyDatabase
from src.database_management.borrow_history_table import BorrowHistoryTable
from src.database_management.book_table import BookTable


@pytest.fixture
def default_setup_teardown():
    """
    default setup / teardown

    Yield
    ----------
    BorrowHistoryTable reference
    """
    # setup
    verbosity = None
    log_ref = LogManagement(verbosity, os.path.basename(__file__))
    db_mgmt = LeafyDatabase(log_ref)
    db_mgmt.start_database_engine()
    book_ref = BookTable(log_ref, db_mgmt)
    borrow_history_ref = BorrowHistoryTable(log_ref, db_mgmt)

    # provide the data to the test
    yield borrow_history_ref, book_ref

    # teardown
    db_mgmt.delete_database_permanentely()


@pytest.mark.parametrize(
    "release_date,return_date",
    [
        (None, None),
        (None, date.fromisoformat("2019-12-04")),
        (date.fromisoformat("2024-12-04"), date.fromisoformat("2019-12-04")),
        (date.fromisoformat("2019-12-04"), None),
    ],
)
def test_create_borrow_history(
    default_setup_teardown, release_date, return_date
) -> None:
    borrow_history_ref, book_ref = default_setup_teardown
    assert borrow_history_ref is not None
    book_info: Book = book_ref.create_book(title="a@a.a", author="0")

    my_borrow_history: BorrowHistory = borrow_history_ref.create_borrow_history(
        book=book_info, release_date=release_date, return_date=return_date
    )
    assert my_borrow_history.return_date == return_date
    if release_date is not None:
        assert my_borrow_history.release_date.strftime(
            "%Y%m%d"
        ) == release_date.strftime("%Y%m%d")
    else:
        assert my_borrow_history.release_date.strftime(
            "%Y%m%d"
        ) == datetime.today().strftime("%Y%m%d")
    if return_date is not None:
        assert my_borrow_history.return_date.strftime("%Y%m%d") == return_date.strftime(
            "%Y%m%d"
        )
    else:
        assert my_borrow_history.return_date is None


def test_get_borrow_history_list(default_setup_teardown) -> None:
    borrow_history_ref, book_ref = default_setup_teardown
    assert borrow_history_ref is not None
    date_1 = date.fromisoformat("2019-12-04")
    date_2 = date.fromisoformat("1994-01-01")
    book_1 = book_ref.create_book(title="a@a.a", author="0")
    book_2 = book_ref.create_book(
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
    book_3 = book_ref.create_book(
        title="a@a.a", author="0", available=True, archived=False
    )
    borrow_history_1_0 = borrow_history_ref.create_borrow_history(book=book_1)
    borrow_history_1_1 = borrow_history_ref.create_borrow_history(
        book=book_1,
        release_date=date_1,
    )
    borrow_history_1_2 = borrow_history_ref.create_borrow_history(
        book=book_1,
        release_date=date_2,
        return_date=date_1,
    )
    borrow_history_2_0 = borrow_history_ref.create_borrow_history(
        book=book_2,
        release_date=date_2,
        return_date=date_1,
    )
    borrow_history_2_1 = borrow_history_ref.create_borrow_history(
        book=book_2,
    )
    borrow_history_2_2 = borrow_history_ref.create_borrow_history(
        book=book_2,
    )
    borrow_history_3 = borrow_history_ref.create_borrow_history(
        book=book_3,
        return_date=date_1,
    )

    borrow_history_list = borrow_history_ref.get_borrow_history_list(book=book_2)
    assert len(borrow_history_list) == 3
    assert borrow_history_2_0 in borrow_history_list
    assert borrow_history_2_1 in borrow_history_list
    assert borrow_history_2_2 in borrow_history_list

    borrow_history_list = borrow_history_ref.get_borrow_history_list(
        release_date=date_2
    )
    assert len(borrow_history_list) == 2
    assert borrow_history_1_2 in borrow_history_list
    assert borrow_history_2_0 in borrow_history_list

    borrow_history_list = borrow_history_ref.get_borrow_history_list(return_date=date_1)
    assert len(borrow_history_list) == 3
    assert borrow_history_1_2 in borrow_history_list
    assert borrow_history_2_0 in borrow_history_list
    assert borrow_history_3 in borrow_history_list

    borrow_history_list = borrow_history_ref.get_borrow_history_list()
    assert len(borrow_history_list) == 7
    assert borrow_history_1_0 in borrow_history_list
    assert borrow_history_1_1 in borrow_history_list
    assert borrow_history_1_2 in borrow_history_list
    assert borrow_history_2_0 in borrow_history_list
    assert borrow_history_2_1 in borrow_history_list
    assert borrow_history_2_2 in borrow_history_list
    assert borrow_history_3 in borrow_history_list


@pytest.mark.parametrize(
    "init_release_date,init_return_date",
    [
        (
            None,
            None,
        ),
        (
            date.fromisoformat("2019-12-04"),
            date.fromisoformat("2024-12-04"),
        ),
    ],
)
@pytest.mark.parametrize(
    "new_book,release_date,return_date",
    [
        (
            False,
            None,
            None,
        ),
        (
            True,
            None,
            None,
        ),
        (
            False,
            date.fromisoformat("2019-12-04"),
            None,
        ),
        (
            False,
            None,
            date.fromisoformat("2019-12-04"),
        ),
        (
            True,
            date.fromisoformat("2019-01-10"),
            date.fromisoformat("2019-05-31"),
        ),
    ],
)
def test_update_borrow_history(
    default_setup_teardown,
    init_release_date,
    init_return_date,
    new_book,
    release_date,
    return_date,
) -> None:
    borrow_history_ref, book_ref = default_setup_teardown
    assert borrow_history_ref is not None
    init_book_info = book_ref.create_book(title="a@a.a", author="0")
    new_book_info = book_ref.create_book(
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

    my_borrow_history: BorrowHistory = borrow_history_ref.create_borrow_history(
        book=init_book_info,
        release_date=init_release_date,
        return_date=init_return_date,
    )

    if new_book is True:
        book_info = new_book_info
    else:
        book_info = None

    my_borrow_history: BorrowHistory = borrow_history_ref.update_borrow_history(
        my_borrow_history,
        book=book_info,
        release_date=release_date,
        return_date=return_date,
    )

    if new_book is False:
        borrow_history_list = borrow_history_ref.get_borrow_history_list(
            book=init_book_info
        )
        assert len(borrow_history_list) == 1
        borrow_history_list = borrow_history_ref.get_borrow_history_list(
            book=new_book_info
        )
        assert len(borrow_history_list) == 0
    else:
        borrow_history_list = borrow_history_ref.get_borrow_history_list(
            book=init_book_info
        )
        assert len(borrow_history_list) == 0
        borrow_history_list = borrow_history_ref.get_borrow_history_list(
            book=new_book_info
        )
        assert len(borrow_history_list) == 1
    if release_date is None:
        if init_release_date is not None:
            assert my_borrow_history.release_date == init_release_date
        else:
            assert my_borrow_history.release_date.strftime(
                "%Y%m%d"
            ) == datetime.today().strftime("%Y%m%d")
    else:
        assert my_borrow_history.release_date == release_date
    if return_date is None:
        assert my_borrow_history.return_date == init_return_date
    else:
        assert my_borrow_history.return_date == return_date


@pytest.mark.parametrize(
    "release_date,return_date",
    [
        (
            None,
            None,
        ),
        (
            date.fromisoformat("2019-12-04"),
            date.fromisoformat("2024-12-04"),
        ),
    ],
)
def test_delete_borrow_history(
    default_setup_teardown, release_date, return_date
) -> None:
    borrow_history_ref, book_ref = default_setup_teardown
    assert borrow_history_ref is not None
    book_info = book_ref.create_book(title="a@a.a", author="0")
    my_borrow_history: BorrowHistory = borrow_history_ref.create_borrow_history(
        book=book_info, release_date=release_date, return_date=return_date
    )

    borrow_history_list = borrow_history_ref.get_borrow_history_list(book=book_info)
    assert len(borrow_history_list) == 1

    borrow_history_ref.delete_borrow_history(my_borrow_history)

    borrow_history_list = borrow_history_ref.get_borrow_history_list(book=book_info)
    assert len(borrow_history_list) == 0
