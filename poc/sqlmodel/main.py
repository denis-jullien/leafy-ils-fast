import argparse
import logging

from sqlmodel import Session, select

from .src import *

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


    # Print table from database
    log_level = log_ref.get_logging_level()
    if log_level == logging.INFO or log_level == logging.DEBUG:
        with Session(database_engine) as session:
            for cl in [Family, FamilyMember, Book, BorrowHistory]:
                log_ref.get_logger().info(f"\n\n{cl}: \n")
                statement = select(cl)
                results = session.exec(statement)
                for elem in results:
                    log_ref.get_logger().info(f"{elem}")

    # TODO: remove later
    leafy_database.delete_database_permanentely()
