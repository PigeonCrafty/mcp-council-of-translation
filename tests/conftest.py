"""
Pytest configuration and shared fixtures for Council of Translation tests
"""

import sys
from pathlib import Path

# Add src package directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
