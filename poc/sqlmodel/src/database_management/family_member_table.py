from datetime import date

from sqlmodel import Session, select

from src.database_management.tables_definition import Family, FamilyMember
from src.database_management.leafy_database import LeafyDatabase
from src.tools.log_management import LogManagement


class FamilyMemberTable:
    """
    A class used to manage the FamilyMember table
    """

    def __init__(self, log_ref: LogManagement, db: LeafyDatabase) -> None:
        """Initialize the class

        Parameters
        ----------
            log_ref: log management reference
            db: database reference
        """
        self._log_ref = log_ref
        self._db = db
        self._db_engine = self._db.get_database_engine()

    def create_family_member(
        self,
        family: Family,
        firstname: str,
        surname: str,
        birthdate: date | None = None,
        family_referent: bool = False,
    ) -> FamilyMember:
        """Create family member

        Parameters
        ----------
            family: should have been created through FamilyTable
            firstname: member's firsname
            surname: member's surname
            birthdate: member's birthdate
            family_referent: indicate if the member is the referent of its family

        Returns
        ----------
            member reference
        """
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

    def get_family_member_list(
        self,
        family: Family | None = None,
        firstname: str | None = None,
        surname: str | None = None,
        birthdate: date | None = None,
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
        return member_list

    def update_family_member(
        self,
        member: FamilyMember,
        family: Family | None = None,
        firstname: str | None = None,
        surname: str | None = None,
        birthdate: date | None = None,
        family_referent: bool | None = None,
    ) -> FamilyMember:
        """Update family member

        Parameters
        ----------
            member: member reference
            family
            firstname
            surname
            birthdate
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
        if birthdate is not None:
            member.birthdate = birthdate
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
        """Delete a family member

        Parameters
        ----------
            member reference
        """
        with Session(self._db_engine) as session:
            session.delete(member)
            session.commit()
        self._log_ref.get_logger().info(f"delete family member: {member}")
