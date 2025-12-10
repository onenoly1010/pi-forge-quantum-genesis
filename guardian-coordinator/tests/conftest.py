"""
Pytest configuration for guardian-coordinator tests.
Sets up proper module paths for importing guardian modules.
"""

import sys
import os

# Add parent directory to path for test imports
GUARDIAN_DIR = os.path.dirname(os.path.dirname(__file__))
if GUARDIAN_DIR not in sys.path:
    sys.path.insert(0, GUARDIAN_DIR)
