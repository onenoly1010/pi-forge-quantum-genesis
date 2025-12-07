"""
Pytest configuration for Pi Forge Quantum Genesis tests.
Sets up proper module paths for importing server modules.
"""

import sys
import os

# Add server directory to path for test imports
SERVER_DIR = os.path.join(os.path.dirname(__file__), '..', 'server')
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)
