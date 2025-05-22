"""
Nim Misere Game Simulation UI
Run this script to start the Nim Misere simulation interface.
"""

import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Ui.NimMisereApp import NimMisereApp


if __name__ == "__main__":
    app = NimMisereApp()
    app.run()
