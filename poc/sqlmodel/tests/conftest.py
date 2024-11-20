# tests/conftest.py
import sys
from pathlib import Path

# Add the src directory to sys.path for all test files
project_root = Path(__file__).resolve().parents[1]  # Navigate to the root directory
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))
