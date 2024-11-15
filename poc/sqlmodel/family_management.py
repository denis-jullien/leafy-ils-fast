import argparse
import datetime
import logging
import pytest

from sqlmodel import Session, select

from database_definition import Family, FamilyMember
from leafy_database import LeafyDatabase
from log_management import LogManagement


class FamilyManagement:
    """
    A class used to manage the family and its members
    """

    def __init__(self, log_ref: LogManagement, db: LeafyDatabase) -> None:
        """Initialize the class to manage the Family and FamilyMember database's tables

        Parameters
        ----------
        log_ref: log management reference
        db: database reference
        """
        self._log_ref = log_ref
        self._db = db
        self._db_engine = self._db.get_database_engine()

    def get_family_list(
        self,
        email: str | None = None,
        phone_number: str | None = None,
    ) -> list[Family]:
        """Get list of family's references

        Parameters
        ----------
        email: if not None, search for family by email
        phone_number: if not None, search for family by phone_number

        Returns
        ----------
        list of family's references depending of the parameters
        """
        with Session(self._db_engine) as session:
            # Get all base
            statement = select(Family)

            # mapping of value to look for with column names
            search_mapping = [
                (email, Family.email),
                (phone_number, Family.phone_number),
            ]
            statement = self._db.search_table_elements(statement, search_mapping)

            results = session.exec(statement)
            family_list = results.all()
        return family_list

    def create_family(
        self,
        email: str | None = None,
        phone_number: str | None = None,
    ) -> Family:
        """Create a family
        at least one of email or phone_number must be present

        Parameters
        ----------
        phone_number
        email

        Returns
        ----------
        family reference
        """
        if phone_number is None and email is None:
            raise NameError(
                f"At least one contact information must be set among phone_number '{phone_number}' and email '{email}'."
            )

        last_adhesion_date = datetime.datetime.today()
        family = Family(
            email=email,
            phone_number=phone_number,
            last_adhesion_date=last_adhesion_date,
        )
        with Session(self._db_engine) as session:
            session.add(family)
            session.commit()
            session.refresh(family)
        self._log_ref.get_logger().info(f"create family: {family}")
        return family

    def update_family(
        self,
        family: Family,
        email: str | None = None,
        phone_number: str | None = None,
        last_adhesion_date: datetime.date | None = None,
    ):
        """Update a family
        at least one of email or phone_number must be present

        Parameters
        ----------
        family: family to update reference
        phone_number
        email
        last_adhesion_date

        Returns
        ----------
        family reference
        """
        if email is not None:
            family.email = email
        if phone_number is not None:
            family.phone_number = phone_number
        if last_adhesion_date is not None:
            family.last_adhesion_date = last_adhesion_date

        if (family.phone_number is None or family.phone_number == "") and (
            family.email is None or family.email == ""
        ):
            raise NameError(
                f"At least one contact information must be set among phone_number '{family.phone_number}' and email '{family.email}'."
            )

        with Session(self._db_engine) as session:
            session.add(family)
            session.commit()
            session.refresh(family)
        self._log_ref.get_logger().info(f"update family: {family}")
        return family

    def delete_family(self, family: Family) -> None:
        """Delete a family

        Parameters
        ----------
        family: family to update reference
        """
        with Session(self._db_engine) as session:
            session.delete(family)
            session.commit()
        self._log_ref.get_logger().info(f"delete family: {family}")

    def get_family_member_list(
        self,
        family: Family | None = None,
        firstname: str | None = None,
        surname: str | None = None,
        birthdate: str | None = None,
        family_referent: bool | None = None,
    ) -> list[FamilyMember]:
        """Get list of family member's references

        Parameters
        ----------
        family: if not None, search for member by family
        firstname: if not None, search for family by firstname
        surname: if not None, search for member by surname
        birthdate: if not None, search for member by birthdate
        family_referent: if not None, search for member by family_referent

        Returns
        ----------
        list of family member's references depending of the parameters
        """
        with Session(self._db_engine) as session:
            # Get all base
            statement = select(FamilyMember)

            # mapping of value to look for with column names
            search_mapping = [
                (firstname, FamilyMember.firstname),
                (surname, FamilyMember.surname),
                (birthdate, FamilyMember.birthdate),
                (family_referent, FamilyMember.family_referent),
            ]
            if family is not None:
                search_mapping.append((family.id, FamilyMember.family_id))
            statement = self._db.search_table_elements(statement, search_mapping)

            results = session.exec(statement)
            member_list = results.all()
        return  member_list

    def create_family_member(
        self,
        family: Family,
        firstname: str,
        surname: str,
        birthdate: str | None = None,
        family_referent: bool = False,
    ) -> FamilyMember:
        """Create family member

        Parameters
        ----------
        family
        firstname
        surname
        birthdate: format should be YYYY-MM-DD
        family_referent

        Returns
        ----------
        member reference
        """
        if birthdate != None:
            birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
        member = FamilyMember(
            family=family,
            firstname=firstname,
            surname=surname,
            birthdate=birthdate,
            family_referent=family_referent,
        )
        with Session(self._db_engine) as session:
            session.add(member)
            session.commit()
            session.refresh(member)
            session.refresh(family)
        self._log_ref.get_logger().info(f"create family member: {member}")
        return member

    def update_family_member(
        self,
        member: FamilyMember,
        family: Family | None = None,
        firstname: str | None = None,
        surname: str | None = None,
        birthdate: str | None = None,
        family_referent: bool | None = None,
    ) -> FamilyMember:
        """Update family member

        Parameters
        ----------
        member
        family
        firstname
        surname
        birthdate: format should be YYYY-MM-DD
        family_referent

        Returns
        ----------
        member reference
        """
        if family is not None:
            member.family = family
        if firstname is not None:
            member.firstname = firstname
        if surname is not None:
            member.surname = surname
        if birthdate != None:
            member.birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
        if family_referent is not None:
            member.family_referent = family_referent

        with Session(self._db_engine) as session:
            session.add(member)
            session.commit()
            session.refresh(member)
            if family is not None:
                session.refresh(family)
        self._log_ref.get_logger().info(f"update family member: {member}")
        return member

    def delete_family_member(self, member: FamilyMember) -> None:
        """Delete a family

        Parameters
        ----------
        member
        """
        with Session(self._db_engine) as session:
            family = member.family
            session.delete(member)
            session.commit()
            if family is not None:
                session.refresh(family)
        self._log_ref.get_logger().info(f"delete family: {member}")


# class TestFamilyManagement:
#     log_ref = LogManagement(None, "test")
#     leafy_database = LeafyDatabase(log_ref)

#     def default_setup(self):
#         """
#         prepare
#         """
#         database_engine = TestFamilyManagement.leafy_database.get_database_engine()
#         family_mgmt = FamilyManagement(TestFamilyManagement.log_ref, database_engine)

#         # provide the data to the test
#         return family_mgmt

#     def default_teardown(self) -> None:
#         TestFamilyManagement.leafy_database.delete_database_permanentely()

#     def test_family_management_init(self):
#         family_mgmt = self.default_setup()
#         assert family_mgmt != None

#         self.default_teardown()

#     @pytest.mark.parametrize("family_details", [
#         {"referent_firstname":"John1", "referent_surname":"Smith", "referent_birthdate":"1994-2-2", "phone_number":"063236564"},
#         # {"referent_firstname":"John2", "referent_surname":"Smith", "referent_birthdate":"1994-2-2", "email":"a@a"},
#         # {"referent_firstname":"John3", "referent_surname":"Smith", "referent_birthdate":"1994-2-2", "phone_number":"063236564", "email":"a@a"},
#                    ])
#     def test_create_family(self, family_details):
#         family_mgmt = self.default_setup()
#         print(f"family_details: {family_details}")
#         family_ref = family_mgmt.create_family(**family_details)
#         assert family_ref != None

#         self.default_teardown()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="""
        """
    )
    argparser.add_argument(
        "-v", "--verbosity", action="count", help="increase output verbosity"
    )
    args = argparser.parse_args()

    log_ref = LogManagement(args.verbosity, "test")

    leafy_database = LeafyDatabase(log_ref)
    leafy_database.start_database_engine()
    database_engine = leafy_database.get_database_engine()

    # Tests
    family_mgmt = FamilyManagement(log_ref, leafy_database)

    family_1 = family_mgmt.create_family(phone_number="063236564")
    family_1 = family_mgmt.update_family(family_1, phone_number="000000000")
    member_1_1 = family_mgmt.create_family_member(
        family_1, "John", "Smith", "1994-2-2", family_referent=True
    )
    family_2 = family_mgmt.create_family(email="a@a")
    member_2_1 = family_mgmt.create_family_member(
        family_2, "John2", "Smith", "1994-2-2", family_referent=True
    )
    family_3 = family_mgmt.create_family(phone_number="063236564", email="a@a")
    member_3_1 = family_mgmt.create_family_member(
        family_3, "John3", "Smith", "1994-2-2"
    )

    member_2_2 = family_mgmt.create_family_member(family_2, "blabla", "Smith")
    member_2_3 = family_mgmt.create_family_member(
        family_2, "blabla2", "Smith"
    )
    member_1_2 = family_mgmt.create_family_member(family_1, "blabla2", "John")
    log_ref.get_logger().info(f"\n\nfamily info: \n")
    log_ref.get_logger().info(f"family_2: {family_2}")

    log_ref.get_logger().info(f"\n\nget_family_member_list: \n")
    member_list = family_mgmt.get_family_member_list(family=family_2)
    log_ref.get_logger().info(f"member_list: {member_list}")
    member_list = family_mgmt.get_family_member_list(surname="Smith")
    log_ref.get_logger().info(f"member_list: {member_list}")
    member_list = family_mgmt.get_family_member_list(family_referent=True)
    log_ref.get_logger().info(f"member_list: {member_list}")
    # family_4 = family_mgmt.create_family("John2", "Smith")

    # Print table from database
    log_level = log_ref.get_logging_level()
    if log_level == logging.INFO or log_level == logging.DEBUG:
        with Session(database_engine) as session:
            for cl in [Family, FamilyMember]:
                log_ref.get_logger().info(f"\n\n{cl}: \n")
                statement = select(cl)
                results = session.exec(statement)
                for elem in results:
                    log_ref.get_logger().info(f"{elem}")

    # TODO: remove later
    leafy_database.delete_database_permanentely()
