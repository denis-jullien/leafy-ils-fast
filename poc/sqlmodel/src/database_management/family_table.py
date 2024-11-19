from datetime import datetime, date

from sqlmodel import Session, select

from src.database_management.tables_definition import Family
from src.database_management.leafy_database import LeafyDatabase
from src.tools.log_management import LogManagement


class FamilyTable:
    """
    A class used to manage the Family table
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

    def create_family(
        self,
        email: str | None = None,
        phone_number: str | None = None,
    ) -> Family:
        """Create a family

        Parameters
        ----------
        phone_number
        email

        Returns
        ----------
        family reference
        """
        last_adhesion_date = datetime.today()
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

    def update_family(
        self,
        family: Family,
        email: str | None = None,
        phone_number: str | None = None,
        last_adhesion_date: date | None = None,
    ):
        """Update a family

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
        family: family reference
        """
        with Session(self._db_engine) as session:
            session.delete(family)
            session.commit()
        self._log_ref.get_logger().info(f"delete family: {family}")
