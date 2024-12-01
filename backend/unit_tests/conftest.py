# conftest.py
# see https://gist.github.com/peterhurford/09f7dcda0ab04b95c026c60fa49c2a68 to introdue modularity
import pytest
import sys
from pathlib import Path

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.database import get_session
from backend.main import app

# Add the src directory to sys.path for all test files
project_root = Path(__file__).resolve().parents[1]  # Navigate to the root directory
sys.path.append(str(project_root))
sys.path.append(str(project_root / "backend"))





@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
