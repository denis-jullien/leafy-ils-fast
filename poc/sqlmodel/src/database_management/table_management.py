from datetime import datetime, date

from sqlalchemy.sql import func
from sqlmodel import Session, select

from src.database_management.models import (
    AuthorTable,
    AuthorCreate,
    AuthorUpdate,
    AuthorSearch,
    BookTable,
    BookCreate,
    BookUpdate,
    BookSearch,
)
from src.database_management.leafy_database import LeafyDatabase
from src.tools.log_management import LogManagement


class TableManagement:
    """
    A class used to manage the author
    """

    TableType = AuthorTable | BookTable
    CreateType = AuthorCreate | BookCreate
    UpdateType = AuthorUpdate | BookUpdate
    SearchType = AuthorSearch | BookSearch

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

        self._class_mapping_create = {AuthorCreate: AuthorTable, BookCreate: BookTable}
        self._class_mapping_search = {AuthorSearch: AuthorTable, BookSearch: BookTable}

    def _generate_mapping(self, data_search: SearchType, db_data_class) -> list:
        """Automatically generate the search mapping, the link between data_search value and db_data_class element

        Parameters
        ----------
        data_search
        db_data_class

        Returns
        ----------
            search_mapping
            ex1:
                search_mapping = [
                    (title, Book.title),
                    (author, Book.author)
                ]
            ex2:
                search_mapping = [
                    (firstname, FamilyMember.firstname),
                    (surname, FamilyMember.surname),
                    (birthdate, FamilyMember.birthdate),
                    (family_referent, FamilyMember.family_referent),
                ]
                if family is not None:
                    search_mapping.append((family.id, FamilyMember.family_id))
        """
        search_mapping = []
        data_search_class = data_search.__class__

        # Get the attributes of search SQLModel class
        data_search_fields = data_search_class.__fields__

        # Generate the mapping
        for field in data_search_fields:
            data_search_value = getattr(data_search, field)
            search_mapping.append((data_search_value, getattr(db_data_class, field)))

        return search_mapping

    def _normalize_string(self, string: str):
        """normalize strings (case-insensitive, remove spaces and special characters)"""
        return func.replace(func.replace(func.lower(string), " ", ""), "-", "")

    def _search_table_elements(self, statement, search_mapping: list):
        """Search elements' table in a statement from a SQLModel select according to search_mapping

        Parameters
        ----------
            statement:
                result of SQLModel select
                ex: statement = select(Book)
            search_mapping
                dynamically add filters based on non-None arguments

        Returns
        ----------
            statement updated
        """
        for value, column in search_mapping:
            if value is not None:
                statement = statement.where(
                    self._normalize_string(column).contains(
                        self._normalize_string(value)
                    )
                )
        return statement

    def create_data(
        self,
        data: CreateType,
    ) -> TableType:
        """Create an element in a table from the database
        TODO: deal with relationship

        Parameters
        ----------
        data: data to save in database

        Returns
        ----------
        table reference related to the data in the entry
        """
        self._log_ref.get_logger().debug(f"create data: {data}")
        data_class = data.__class__
        db_data_class = self._class_mapping_create[data_class]

        with Session(self._db_engine) as session:
            db_data = db_data_class.model_validate(data)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
        self._log_ref.get_logger().info(f"data created: {db_data}")
        return db_data

    def get_data_list(
        self,
        data_search: SearchType,
    ) -> TableType:
        """Get list of data's references
        TODO: deal with relationship
        TODO: deal with date range
        TODO: add pagination https://sqlmodel.tiangolo.com/tutorial/fastapi/limit-and-offset/#add-a-limit-and-offset-to-the-query-parameters

        Parameters
        ----------
            data_search: data to use for search, the parameters used will be those that are not equal to None

        Returns
        ----------
            list of data's references depending of the search
        """

        self._log_ref.get_logger().debug(f"search data: {data_search}")
        data_search_class = data_search.__class__
        db_data_class = self._class_mapping_search[data_search_class]
        with Session(self._db_engine) as session:
            # Get all base
            statement = select(db_data_class)

            # mapping of value to look for with column names
            search_mapping = self._generate_mapping(data_search, db_data_class)
            # if family is not None:
            #     search_mapping.append((family.id, FamilyMember.family_id))
            statement = self._search_table_elements(statement, search_mapping)

            results = session.exec(statement)
            member_list = results.all()
        return member_list

    def get_data(self, id: int, cls) -> TableType:
        """Get an element in a table from the database with its id"""
        with Session(self._db_engine) as session:
            element = session.get(cls, id)
        return element

    def update_data(self, db_data: TableType, new_data: UpdateType) -> TableType:
        """Update an element in a table from the database
        TODO: deal with relationship

        Parameters
        ----------
        db_data: data to update
        new_data: data to use for update, the parameters updated will be those that are not equal to None

        Returns
        ----------
        table reference related to the data in the entry
        """
        self._log_ref.get_logger().debug(f"update data: {db_data} with {new_data}")
        with Session(self._db_engine) as session:
            data = new_data.model_dump(exclude_unset=True, exclude_none=True)
            db_data.sqlmodel_update(data)
            session.add(db_data)
            session.commit()
            session.refresh(db_data)
        self._log_ref.get_logger().info(f"data updated: {db_data}")
        return db_data

    def delete_data(self, db_data: TableType) -> None:
        """Delete an element in a table from the database

        Parameters
        ----------
        db_data: data to delete
        """
        self._log_ref.get_logger().debug(f"delete data: {db_data}")
        with Session(self._db_engine) as session:
            session.delete(db_data)
            session.commit()
        self._log_ref.get_logger().info(f"data deleted: {db_data}")

    def make_link(self, data_1: BookTable, data_2: AuthorTable):
        print(f"data_1: {data_1}")
        print(f"data_2: {data_2}")
        with Session(self._db_engine) as session:
            book = session.get(BookTable, data_1.id)
            author = session.get(AuthorTable, data_2.id)
            # book = data_1
            # author = data_2
            book.authors.append(author)
            session.add(book)
            session.commit()
            session.refresh(book)
            session.refresh(author)
            print(f"book_link authors: {book.authors}")
            print(f"author_link books: {author.books}")
        return book, author
