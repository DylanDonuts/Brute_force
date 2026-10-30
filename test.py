"""Avvio compatibile con il comando storico: python test.py.

I test correnti sono in tests/. Le copie ricevute restano in originali/.
"""
from pathlib import Path
import unittest


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
