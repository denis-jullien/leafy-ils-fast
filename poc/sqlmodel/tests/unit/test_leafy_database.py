import os
import pytest

from src.tools.log_management import LogManagement
from src.database_management.leafy_database import LeafyDatabase


@pytest.fixture
def default_setup_teardown(request):
    """
    default setup / teardown

    Parameters
    ----------
        debug (bool): False by default
        db_name (str): None by default

    Yield
    ----------
    LeafyDatabase reference, LeafyDatabase name
    """
    debug = False
    db_name = None
    if hasattr(request, "param"):
        args = request.param
        if "debug" in args:
            debug = args["debug"]
        if "db_name" in args:
            db_name = args["db_name"]

    # setup
    if debug is False:
        verbosity = 4
    else:
        verbosity = None
    log_ref = LogManagement(verbosity, os.path.basename(__file__))

    if db_name is None:
        db_mgmt = LeafyDatabase(log_ref)
        db_name = LeafyDatabase.DEFAULT_DATABASE_NAME
    else:
        db_mgmt = LeafyDatabase(log_ref, database_name=db_name)

    # provide the data to the test
    yield db_mgmt, db_name

    # teardown
    if os.path.isfile(db_name):
        os.remove(db_name)


@pytest.mark.parametrize(
    "default_setup_teardown",
    [{"debug": False, "db_name": None}, {"debug": True, "db_name": None}],
    indirect=True,
)
def test_init(default_setup_teardown) -> None:
    db_mgmt, _ = default_setup_teardown
    assert db_mgmt is not None


def test_get_database_engine(default_setup_teardown) -> None:
    db_mgmt, _ = default_setup_teardown
    db_engine = db_mgmt.get_database_engine()
    assert db_engine is not None


@pytest.mark.parametrize(
    "default_setup_teardown", [{"db_name": None}, {"db_name": "test.db"}], indirect=True
)
def test_start_database_engine(default_setup_teardown) -> None:
    db_mgmt, db_name = default_setup_teardown

    assert os.path.isfile(db_name) is False
    db_mgmt.start_database_engine()
    assert os.path.isfile(db_name) is True


@pytest.mark.parametrize(
    "default_setup_teardown", [{"db_name": None}, {"db_name": "test.db"}], indirect=True
)
def test_remove_database_engine(default_setup_teardown) -> None:
    db_mgmt, db_name = default_setup_teardown
    db_mgmt.start_database_engine()

    assert os.path.isfile(db_name) is True
    db_mgmt.delete_database_permanentely()
    assert os.path.isfile(db_name) is False
