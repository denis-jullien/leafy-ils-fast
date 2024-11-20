from datetime import datetime, date
import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.tables_definition import Book, EMPTY_STRING
from src.database_management.leafy_database import LeafyDatabase
from src.database_management.book_table import BookTable


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
    book_ref = BookTable(log_ref, db_mgmt)

    # provide the data to the test
    yield book_ref

    # teardown
    db_mgmt.delete_database_permanentely()


@pytest.mark.parametrize(
    "title,author,synopsis,edition,catalog,category_type,category_age,category_topics,langage,cover,available,archived,registration_date",
    [
        (
            "title",
            "author",
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            None,
            True,
            False,
            None,
        ),
        (
            "title",
            "author",
            "synopsis",
            "edition",
            "catalog",
            "category_type",
            "category_age",
            "category_topics",
            "langage",
            "cover",
            False,
            True,
            date.fromisoformat("2019-12-04"),
        ),
    ],
)
def test_create_book(
    default_setup_teardown,
    title,
    author,
    synopsis,
    edition,
    catalog,
    category_type,
    category_age,
    category_topics,
    langage,
    cover,
    available,
    archived,
    registration_date,
) -> None:
    book_ref: BookTable = default_setup_teardown
    assert book_ref is not None

    my_book: Book = book_ref.create_book(
        title=title,
        author=author,
        synopsis=synopsis,
        edition=edition,
        catalog=catalog,
        category_type=category_type,
        category_age=category_age,
        category_topics=category_topics,
        langage=langage,
        cover=cover,
        available=available,
        archived=archived,
        registration_date=registration_date,
    )
    assert my_book.title == title
    assert my_book.author == author
    assert my_book.synopsis == synopsis
    assert my_book.edition == edition
    assert my_book.catalog == catalog
    assert my_book.category_type == category_type
    assert my_book.category_age == category_age
    assert my_book.category_topics == category_topics
    assert my_book.langage == langage
    assert my_book.cover == cover
    if registration_date is None:
        assert my_book.registration_date.strftime("%Y%m%d") == datetime.today().strftime(
            "%Y%m%d"
        )
        assert my_book.registration_date.strftime(
            "%Y%m%d%H%M%S%f"
        ) == my_book.last_update_date.strftime("%Y%m%d%H%M%S%f")
    else:
        assert my_book.registration_date.strftime("%Y%m%d") == registration_date.strftime("%Y%m%d")
        assert my_book.last_update_date.strftime("%Y%m%d") == datetime.today().strftime(
            "%Y%m%d"
        )
    assert my_book.available == available
    assert my_book.archived == archived


def test_get_book(default_setup_teardown) -> None:
    book_ref: BookTable = default_setup_teardown
    assert book_ref is not None

    book_1 = book_ref.create_book(
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
    book_3 = book_ref.create_book(title="new", author="author2")
    book_4 = book_ref.create_book(
        title="test", author="test", available=False, archived=False
    )

    book_list = book_ref.get_book_list(title="title")
    assert len(book_list) == 1
    assert book_1 in book_list

    book_list = book_ref.get_book_list(author="author")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_3 in book_list

    book_list = book_ref.get_book_list(synopsis="synopsis")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = book_ref.get_book_list(edition="edition")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = book_ref.get_book_list(catalog="catalog")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = book_ref.get_book_list(category_type="category_type")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = book_ref.get_book_list(category_age="category_age")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = book_ref.get_book_list(category_topics="category_topics")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = book_ref.get_book_list(langage="langage")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = book_ref.get_book_list(cover="")
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_2 in book_list

    book_list = book_ref.get_book_list(available=True)
    assert len(book_list) == 3
    assert book_1 in book_list
    assert book_2 in book_list
    assert book_3 in book_list

    book_list = book_ref.get_book_list(archived=True)
    assert len(book_list) == 1
    assert book_2 in book_list

    book_list = book_ref.get_book_list(available=True, archived=False)
    assert len(book_list) == 2
    assert book_1 in book_list
    assert book_3 in book_list

    book_list = book_ref.get_book_list()
    assert len(book_list) == 4
    assert book_1 in book_list
    assert book_2 in book_list
    assert book_3 in book_list
    assert book_4 in book_list


@pytest.mark.parametrize(
    "init_title,init_author,init_synopsis,init_edition,init_catalog,init_category_type,init_category_age,init_category_topics,init_langage,init_cover,init_available,init_archived",
    [
        (
            "title",
            "author",
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            EMPTY_STRING,
            True,
            False,
        ),
        (
            "title",
            "author",
            "synopsis",
            "edition",
            "catalog",
            "category_type",
            "category_age",
            "category_topics",
            "langage",
            "cover",
            False,
            True,
        ),
    ],
)
@pytest.mark.parametrize(
    "title,author,synopsis,edition,catalog,category_type,category_age,category_topics,langage,cover,available,archived",
    [
        (
            "new",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            None,
            "new",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            None,
            None,
            "new",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            None,
            None,
            None,
            "new",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            None,
            None,
            None,
            None,
            "new",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            None,
            None,
            None,
            None,
            None,
            "new",
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            "new",
            None,
            None,
            None,
            None,
            None,
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "new",
            None,
            None,
            None,
            None,
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "new",
            None,
            None,
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            False,
            None,
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            True,
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "title_new",
            "author_new",
            "synopsis_new",
            "edition_new",
            "catalog_new",
            "category_type_new",
            "category_age_new",
            "category_topics_new",
            "langage_new",
            "cover_new",
            False,
            True,
        ),
    ],
)
def test_update_book(
    default_setup_teardown,
    init_title,
    init_author,
    init_synopsis,
    init_edition,
    init_catalog,
    init_category_type,
    init_category_age,
    init_category_topics,
    init_langage,
    init_cover,
    init_available,
    init_archived,
    title,
    author,
    synopsis,
    edition,
    catalog,
    category_type,
    category_age,
    category_topics,
    langage,
    cover,
    available,
    archived,
) -> None:
    book_ref: BookTable = default_setup_teardown
    assert book_ref is not None

    my_book: Book = book_ref.create_book(
        title=init_title,
        author=init_author,
        synopsis=init_synopsis,
        edition=init_edition,
        catalog=init_catalog,
        category_type=init_category_type,
        category_age=init_category_age,
        category_topics=init_category_topics,
        langage=init_langage,
        cover=init_cover,
        available=init_available,
        archived=init_archived,
    )
    my_book: Book = book_ref.update_book(
        my_book,
        title=title,
        author=author,
        synopsis=synopsis,
        edition=edition,
        catalog=catalog,
        category_type=category_type,
        category_age=category_age,
        category_topics=category_topics,
        langage=langage,
        cover=cover,
        available=available,
        archived=archived,
    )

    if title is None:
        assert my_book.title == init_title
    else:
        assert my_book.title == title
    if author is None:
        assert my_book.author == init_author
    else:
        assert my_book.author == author
    if synopsis is None:
        assert my_book.synopsis == init_synopsis
    else:
        assert my_book.synopsis == synopsis
    if edition is None:
        assert my_book.edition == init_edition
    else:
        assert my_book.edition == edition
    if catalog is None:
        assert my_book.catalog == init_catalog
    else:
        assert my_book.catalog == catalog
    if category_type is None:
        assert my_book.category_type == init_category_type
    else:
        assert my_book.category_type == category_type
    if category_age is None:
        assert my_book.category_age == init_category_age
    else:
        assert my_book.category_age == category_age
    if category_topics is None:
        assert my_book.category_topics == init_category_topics
    else:
        assert my_book.category_topics == category_topics
    if langage is None:
        assert my_book.langage == init_langage
    else:
        assert my_book.langage == langage
    if cover is None:
        assert my_book.cover == init_cover
    else:
        assert my_book.cover == cover
    if available is None:
        assert my_book.available == init_available
    else:
        assert my_book.available == available
    if archived is None:
        assert my_book.archived == init_archived
    else:
        assert my_book.archived == archived

    # Currently, the saving date only includes Year, month and day
    # assert my_book.registration_date.strftime("%Y%m%d%H%M%S%f") != my_book.last_update_date.strftime("%Y%m%d%H%M%S%f")
    assert my_book.last_update_date.strftime("%Y%m%d") == datetime.today().strftime(
        "%Y%m%d"
    )


@pytest.mark.parametrize(
    "title,author,synopsis,edition,catalog,category_type,category_age,category_topics,langage,cover,available,archived",
    [
        (
            "title",
            "author",
            "synopsis",
            "edition",
            "catalog",
            "category_type",
            "category_age",
            "category_topics",
            "langage",
            "cover",
            True,
            False,
        ),
    ],
)
def test_delete_book(
    default_setup_teardown,
    title,
    author,
    synopsis,
    edition,
    catalog,
    category_type,
    category_age,
    category_topics,
    langage,
    cover,
    available,
    archived,
) -> None:
    book_ref: BookTable = default_setup_teardown
    assert book_ref is not None

    my_book: Book = book_ref.create_book(
        title=title,
        author=author,
        synopsis=synopsis,
        edition=edition,
        catalog=catalog,
        category_type=category_type,
        category_age=category_age,
        category_topics=category_topics,
        langage=langage,
        cover=cover,
        available=available,
        archived=archived,
    )

    book_list = book_ref.get_book_list(title=title)
    assert len(book_list) == 1

    book_ref.delete_book(my_book)

    book_list = book_ref.get_book_list(title=title)
    assert len(book_list) == 0
