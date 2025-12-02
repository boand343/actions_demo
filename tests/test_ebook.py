import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.taskClass import EBook


def test_ebook_download():
    b = EBook("Test", "Author", 2010, 5, "pdf")
    msg = b.download()
    assert "Загрузка электронной книги" in msg
    assert "5" in msg
    assert "pdf" in msg
