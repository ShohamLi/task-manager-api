import sys
from pathlib import Path

# Add project root (MY_API) to sys.path so tests can import main.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
