from datetime import datetime, date
import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.tables_definition import Family
from src.database_management.leafy_database import LeafyDatabase
from src.database_management.family_table import FamilyTable


@pytest.fixture
def default_setup_teardown():
    """
    default setup / teardown

    Yield
    ----------
    FamilyTable reference
    """
    # setup
    verbosity = None
    log_ref = LogManagement(verbosity, os.path.basename(__file__))
    db_mgmt = LeafyDatabase(log_ref)
    db_mgmt.start_database_engine()
    family_ref = FamilyTable(log_ref, db_mgmt)

    # provide the data to the test
    yield family_ref

    # teardown
    db_mgmt.delete_database_permanentely()


@pytest.mark.parametrize(
    "email,phone_number",
    [
        ("test_email", "phone_test"),
        ("test@a.a", "003254"),
        ("test_email", None),
        (None, "phone_test"),
        (None, None),
    ],
)
def test_create_family(default_setup_teardown, email, phone_number) -> None:
    family_ref: FamilyTable = default_setup_teardown
    assert family_ref is not None

    my_family: Family = family_ref.create_family(email=email, phone_number=phone_number)
    assert my_family.email == email
    assert my_family.phone_number == phone_number
    assert my_family.last_adhesion_date.strftime("%Y%m%d") == datetime.today().strftime(
        "%Y%m%d"
    )


def test_get_family(default_setup_teardown) -> None:
    family_ref: FamilyTable = default_setup_teardown
    assert family_ref is not None

    family_1 = family_ref.create_family(phone_number="063236564")
    family_2 = family_ref.create_family(email="a@a")
    family_3 = family_ref.create_family(phone_number="063236564", email="a@a")
    family_4 = family_ref.create_family(phone_number=None, email=None)

    family_list = family_ref.get_family_list(email="a@a")
    assert len(family_list) == 2
    assert family_2 in family_list
    assert family_3 in family_list

    family_list = family_ref.get_family_list(phone_number="063236564")
    assert len(family_list) == 2
    assert family_1 in family_list
    assert family_3 in family_list

    family_list = family_ref.get_family_list(email="a@a", phone_number="063236564")
    assert len(family_list) == 1
    assert family_3 in family_list

    family_list = family_ref.get_family_list(email="email")
    assert len(family_list) == 0

    family_list = family_ref.get_family_list()
    assert len(family_list) == 4
    assert family_1 in family_list
    assert family_2 in family_list
    assert family_3 in family_list
    assert family_4 in family_list


@pytest.mark.parametrize(
    "initial_email,initial_phone_number,new_email,new_phone_number,last_adhesion_date",
    [
        ("test@a.a", "003254", None, None, None),
        (None, "003254", "test_email", "phone_test", None),
        ("test@a.a", None, "test_email", "phone_test", None),
        ("test@a.a", "003254", None, "phone_test", None),
        ("test@a.a", "003254", "test_email", None, None),
        (None, "003254", None, "phone_test", None),
        ("test@a.a", None, "test_email", None, None),
        ("test@a.a", "003254", "", "", None),
        ("test@a.a", "003254", None, None, date.fromisoformat("2019-12-04")),
        (
            "test@a.a",
            "003254",
            "test_email",
            "phone_test",
            date.fromisoformat("2019-12-04"),
        ),
    ],
)
def test_update_family(
    default_setup_teardown,
    initial_email,
    initial_phone_number,
    new_email,
    new_phone_number,
    last_adhesion_date,
) -> None:
    family_ref: FamilyTable = default_setup_teardown
    assert family_ref is not None

    my_family: Family = family_ref.create_family(
        email=initial_email, phone_number=initial_phone_number
    )
    my_family: Family = family_ref.update_family(
        my_family,
        email=new_email,
        phone_number=new_phone_number,
        last_adhesion_date=last_adhesion_date,
    )

    if new_email is None:
        assert my_family.email == initial_email
    else:
        assert my_family.email == new_email
    if new_phone_number is None:
        assert my_family.phone_number == initial_phone_number
    else:
        assert my_family.phone_number == new_phone_number
    if last_adhesion_date is None:
        assert my_family.last_adhesion_date.strftime(
            "%Y%m%d"
        ) == datetime.today().strftime("%Y%m%d")
    else:
        assert my_family.last_adhesion_date.strftime(
            "%Y%m%d"
        ) == last_adhesion_date.strftime("%Y%m%d")


@pytest.mark.parametrize(
    "email,phone_number",
    [
        ("test_email", "phone_test"),
    ],
)
def test_delete_family(default_setup_teardown, email, phone_number) -> None:
    family_ref: FamilyTable = default_setup_teardown
    assert family_ref is not None

    my_family: Family = family_ref.create_family(email=email, phone_number=phone_number)
    family_list = family_ref.get_family_list(email=email, phone_number=phone_number)
    assert len(family_list) == 1

    family_ref.delete_family(my_family)

    family_list = family_ref.get_family_list(email=email, phone_number=phone_number)
    assert len(family_list) == 0
