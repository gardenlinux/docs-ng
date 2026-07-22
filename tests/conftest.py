"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

import nltk
import pytest

# Add project root to path so we can import src/aggregation
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture(scope="session", autouse=True)
def download_nltk_data():
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        print("Downloading nltk wordnet data...")
        nltk.download("wordnet", quiet=True)
        nltk.download("omw-1.4", quiet=True)
