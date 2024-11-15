import argparse
import datetime
import logging
import os
from typing import Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from enum import Enum
from pydantic import BaseModel, field_validator, ValidationError, ValidationInfo

from database_definition import Family, FamilyMember
from log_management import LogManagement


class FamilyManagement:
    """
    A class used to manage the family and its members
    """

    def __init__(self, log_ref: LogManagement, db_engine) -> None:
        """Initialize the class to manage the Family and FamilyMember database's tables

        Parameters
        ----------
        log_ref: log management reference
        db_engine: database engine reference
        """
        self._log_ref = log_ref
        self._db_engine = db_engine

    def _create_family_member(
        self, family: Family, firstname: str, surname: str, birthdate: str | None = None
    ):
        """Create family member

        Parameters
        ----------
        family
        firstname
        surname
        birthdate: format should be YYYY-MM-DD

        Returns
        ----------
        member created for database
        """
        if birthdate != None:
            birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
        member = FamilyMember(
            family=family, firstname=firstname, surname=surname, birthdate=birthdate
        )
        self._log_ref.get_logger().info(f"create family member: {member}")
        return member

    def create_new_family(
        self,
        referent_firstname: str,
        referent_surname: str,
        referent_birthdate: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
    ):
        """Create a family
        at least one of email or phone_number must be present

        Parameters
        ----------
        referent_firstname
        referent_surname
        referent_birthdate: format should be YYYY-MM-DD
        phone_number
        email

        Returns
        ----------
        family created for database
        """
        last_adhesion_date = datetime.datetime.today()
        family = Family(
            email=email,
            phone_number=phone_number,
            last_adhesion_date=last_adhesion_date,
        )
        referent_member = self._create_family_member(
            family, referent_firstname, referent_surname, referent_birthdate
        )
        referent_member.family_referent = True
        with Session(self._db_engine) as session:
            session.add(referent_member)
            session.commit()
            session.refresh(family)
        self._log_ref.get_logger().info(f"create family: {family}")
        return family

    def add_family_member(
        self, family: Family, firstname: str, surname: str, birthdate: str | None = None
    ):
        """Add new member to a family

        Parameters
        ----------
        family
        firstname
        surname
        birthdate: format should be YYYY-MM-DD

        Returns
        ----------
        family updated for database
        """
        with Session(self._db_engine) as session:
            new_member = self._create_family_member(
                family, firstname, surname, birthdate
            )
            session.add(new_member)
            session.commit()
            session.refresh(family)
        return family


class LeafyDatabase:
    """
    A class used to manage the database at an high level
    """

    DEFAULT_DATABASE_NAME = "database.db"

    def __init__(
        self, log_ref: LogManagement, database_name: str = DEFAULT_DATABASE_NAME
    ) -> None:
        """Initialize database configuration

        Parameters
        ----------
        log_ref: log management reference
        """
        self._database_name = database_name
        self._log_ref = log_ref
        sqlite_url = f"sqlite:///{self._database_name}"

        if self._log_ref.get_logging_level() == logging.DEBUG:
            engine_echo = True
        else:
            engine_echo = False
        self._engine = create_engine(sqlite_url, echo=engine_echo)

    def start_database_engine(self):
        """Start database engine"""
        SQLModel.metadata.create_all(self._engine)

    def get_database_engine(self):
        """Get database engine reference

        Returns
        ----------
        database engine reference
        """
        return self._engine

    def delete_database_permanentely(self):
        """Delete database engine"""
        os.remove(self._database_name)


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
    family_mgmt = FamilyManagement(log_ref, database_engine)

    family_1 = family_mgmt.create_new_family(
        "John", "Smith", "1994-2-2", phone_number="063236564"
    )
    family_2 = family_mgmt.create_new_family("John2", "Smith", "1994-2-2", email="a@a")
    family_3 = family_mgmt.create_new_family(
        "John3", "Smith", "1994-2-2", phone_number="063236564", email="a@a"
    )
    family_2 = family_mgmt.add_family_member(family_2, "blabla", "Smith")
    family_2 = family_mgmt.add_family_member(family_2, "blabla2", "Smith")
    family_1 = family_mgmt.add_family_member(family_1, "blabla2", "John")

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
