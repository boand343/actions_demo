import os
import sys
from src.taskClass import PrintedBook


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_printed_book_repair():
    b = PrintedBook("T", "A", 2000, 100, "плохая")
    b.repair()
    assert "хорошая" in str(b)
    b.repair()
    assert "новая" in str(b)
