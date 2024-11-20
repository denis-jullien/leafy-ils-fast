from datetime import datetime, date
import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.tables_definition import Family, FamilyMember
from src.database_management.leafy_database import LeafyDatabase
from src.database_management.family_member_table import FamilyMemberTable
from src.database_management.family_table import FamilyTable


@pytest.fixture
def default_setup_teardown():
    """
    default setup / teardown

    Yield
    ----------
    FamilyMemberTable reference
    """
    # setup
    verbosity = None
    log_ref = LogManagement(verbosity, os.path.basename(__file__))
    db_mgmt = LeafyDatabase(log_ref)
    db_mgmt.start_database_engine()
    family_ref = FamilyTable(log_ref, db_mgmt)
    member_ref = FamilyMemberTable(log_ref, db_mgmt)

    # provide the data to the test
    yield member_ref, family_ref

    # teardown
    db_mgmt.delete_database_permanentely()


@pytest.mark.parametrize(
    "firstname,surname,birthdate,family_referent",
    [
        ("firstname", "surname", None, False),
        ("firstname", "surname", datetime.today(), False),
        ("firstname", "surname", date.fromisoformat("2019-12-04"), True),
    ],
)
def test_create_family_member(
    default_setup_teardown, firstname, surname, birthdate, family_referent
) -> None:
    member_ref, family_ref = default_setup_teardown
    assert member_ref is not None
    family_info: Family = family_ref.create_family(email="a@a.a", phone_number="0")

    my_member: FamilyMember = member_ref.create_family_member(
        family=family_info,
        firstname=firstname,
        surname=surname,
        birthdate=birthdate,
        family_referent=family_referent,
    )
    assert my_member.firstname == firstname
    assert my_member.surname == surname
    if birthdate is not None:
        assert my_member.birthdate.strftime("%Y%m%d") == birthdate.strftime("%Y%m%d")
    else:
        assert my_member.birthdate is None
    assert my_member.family_referent == family_referent


def test_get_family_member_list(default_setup_teardown) -> None:
    member_ref, family_ref = default_setup_teardown
    assert member_ref is not None
    date_1 = date.fromisoformat("2019-12-04")
    date_2 = date.fromisoformat("1994-01-01")
    family_1 = family_ref.create_family(phone_number="063236564")
    family_2 = family_ref.create_family(email="a@a")
    family_3 = family_ref.create_family(email="a@a")
    member_1_0 = member_ref.create_family_member(
        family=family_1,
        firstname="firstname1",
        surname="surname",
        birthdate=date_1,
        family_referent=True,
    )
    member_1_1 = member_ref.create_family_member(
        family=family_1,
        firstname="firstname2",
        surname="surname",
        birthdate=date_1,
        family_referent=False,
    )
    member_1_2 = member_ref.create_family_member(
        family=family_1,
        firstname="firstname3",
        surname="another",
        birthdate=date_2,
        family_referent=False,
    )
    member_2_0 = member_ref.create_family_member(
        family=family_2,
        firstname="firstname4",
        surname="a",
        birthdate=date_1,
        family_referent=True,
    )
    member_2_1 = member_ref.create_family_member(
        family=family_2,
        firstname="firstname5",
        surname="a",
        birthdate=date_1,
        family_referent=False,
    )
    member_2_2 = member_ref.create_family_member(
        family=family_2,
        firstname="firstname6",
        surname="a",
        birthdate=date_1,
        family_referent=True,
    )
    member_3 = member_ref.create_family_member(
        family=family_3,
        firstname="firstname7",
        surname="surname",
        birthdate=date_1,
        family_referent=False,
    )

    member_list = member_ref.get_family_member_list(family=family_2)
    assert len(member_list) == 3
    assert member_2_0 in member_list
    assert member_2_1 in member_list
    assert member_2_2 in member_list

    member_list = member_ref.get_family_member_list(firstname="firstname1")
    assert len(member_list) == 1
    assert member_1_0 in member_list

    member_list = member_ref.get_family_member_list(surname="surname")
    assert len(member_list) == 3
    assert member_1_0 in member_list
    assert member_1_1 in member_list
    assert member_3 in member_list

    member_list = member_ref.get_family_member_list(birthdate=date_2)
    assert len(member_list) == 1
    assert member_1_2 in member_list

    member_list = member_ref.get_family_member_list(family_referent=True)
    assert len(member_list) == 3
    assert member_1_0 in member_list
    assert member_2_0 in member_list
    assert member_2_2 in member_list

    member_list = member_ref.get_family_member_list(
        family=family_2, family_referent=True
    )
    assert len(member_list) == 2
    assert member_2_0 in member_list
    assert member_2_2 in member_list

    member_list = member_ref.get_family_member_list()
    assert len(member_list) == 7
    assert member_1_0 in member_list
    assert member_1_1 in member_list
    assert member_1_2 in member_list
    assert member_2_0 in member_list
    assert member_2_1 in member_list
    assert member_2_2 in member_list
    assert member_3 in member_list


@pytest.mark.parametrize(
    "init_firstname,init_surname,init_birthdate,init_family_referent,new_family,firstname,surname,birthdate,family_referent",
    [
        (
            "firstname",
            "surname",
            date.fromisoformat("2019-12-04"),
            False,
            False,
            None,
            None,
            None,
            None,
        ),
        (
            "firstname",
            "surname",
            date.fromisoformat("2019-12-04"),
            False,
            True,
            None,
            None,
            None,
            None,
        ),
        (
            "firstname",
            "surname",
            date.fromisoformat("2019-12-04"),
            False,
            False,
            "new_firstname",
            None,
            None,
            None,
        ),
        (
            "firstname",
            "surname",
            date.fromisoformat("2019-12-04"),
            False,
            False,
            None,
            "new_surname",
            None,
            None,
        ),
        (
            "firstname",
            "surname",
            date.fromisoformat("2019-12-04"),
            False,
            False,
            None,
            None,
            date.fromisoformat("1994-12-04"),
            None,
        ),
        (
            "firstname",
            "surname",
            None,
            False,
            False,
            None,
            None,
            date.fromisoformat("1994-12-04"),
            None,
        ),
        (
            "firstname",
            "surname",
            date.fromisoformat("2019-12-04"),
            False,
            False,
            None,
            None,
            None,
            True,
        ),
        (
            "firstname",
            "surname",
            date.fromisoformat("2019-12-04"),
            True,
            True,
            "new_firstname",
            "new_surname",
            date.fromisoformat("1994-12-04"),
            False,
        ),
    ],
)
def test_update_family_member(
    default_setup_teardown,
    init_firstname,
    init_surname,
    init_birthdate,
    init_family_referent,
    new_family,
    firstname,
    surname,
    birthdate,
    family_referent,
) -> None:
    member_ref, family_ref = default_setup_teardown
    assert member_ref is not None
    init_family_info: Family = family_ref.create_family(email="a@a.a", phone_number="0")
    new_family_info: Family = family_ref.create_family(email="a@a.a")

    my_member: FamilyMember = member_ref.create_family_member(
        family=init_family_info,
        firstname=init_firstname,
        surname=init_surname,
        birthdate=init_birthdate,
        family_referent=init_family_referent,
    )

    if new_family is True:
        family_info = new_family_info
    else:
        family_info = None

    my_member: FamilyMember = member_ref.update_family_member(
        my_member,
        family=family_info,
        firstname=firstname,
        surname=surname,
        birthdate=birthdate,
        family_referent=family_referent,
    )

    if new_family is False:
        member_list = member_ref.get_family_member_list(family=init_family_info)
        assert len(member_list) == 1
        member_list = member_ref.get_family_member_list(family=new_family_info)
        assert len(member_list) == 0
    else:
        member_list = member_ref.get_family_member_list(family=init_family_info)
        assert len(member_list) == 0
        member_list = member_ref.get_family_member_list(family=new_family_info)
        assert len(member_list) == 1
    if firstname is None:
        assert my_member.firstname == init_firstname
    else:
        assert my_member.firstname == firstname
    if surname is None:
        assert my_member.surname == init_surname
    else:
        assert my_member.surname == surname
    if birthdate is None:
        assert my_member.birthdate == init_birthdate
    else:
        assert my_member.birthdate == birthdate
    if family_referent is None:
        assert my_member.family_referent == init_family_referent
    else:
        assert my_member.family_referent == family_referent


@pytest.mark.parametrize(
    "firstname,surname,birthdate,family_referent",
    [
        ("firstname", "surname", None, False),
        ("firstname", "surname", date.fromisoformat("2019-12-04"), True),
    ],
)
def test_delete_family_member(
    default_setup_teardown, firstname, surname, birthdate, family_referent
) -> None:
    member_ref, family_ref = default_setup_teardown
    assert member_ref is not None
    family_info: Family = family_ref.create_family(email="a@a.a", phone_number="0")
    my_member: FamilyMember = member_ref.create_family_member(
        family=family_info,
        firstname=firstname,
        surname=surname,
        birthdate=birthdate,
        family_referent=family_referent,
    )

    member_list = member_ref.get_family_member_list(family=family_info)
    assert len(member_list) == 1

    member_ref.delete_family_member(my_member)

    member_list = member_ref.get_family_member_list(family=family_info)
    assert len(member_list) == 0
