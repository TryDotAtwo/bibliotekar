"""
Test configuration for pytest to ensure the bibliotekar package is importable.
"""
import sys
from pathlib import Path

# Add the project root to sys.path so that 'bibliotekar' is importable
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))