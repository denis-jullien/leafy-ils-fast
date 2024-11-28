from sqlmodel import SQLModel, create_engine, Session

DEFAULT_DATABASE_NAME = "database.db"

database_name = DEFAULT_DATABASE_NAME
sqlite_url = f"sqlite:///{database_name}"

# Create database engine
engine_echo = False
connect_args = {"check_same_thread": False}  # to work with FastAPI
global_engine = create_engine(sqlite_url, echo=engine_echo, connect_args=connect_args)


# Start database engine
def create_db_and_tables() -> None:
    """Create database and the its tables"""
    SQLModel.metadata.create_all(global_engine)


def get_session():
    """Get session for FastAPI Dependency"""
    with Session(global_engine) as session:
        yield session
