"""
"""

from pathlib import Path

def read_file_if_exists(module_file: str, filename: str, encoding: str = 'utf-8'):
    """
    Check if the file at the given path is readable, if yes return its contents.
    If no, return empty string.
    """
    p = Path(module_file).with_name(filename)
    return p.read_text(encoding=encoding) if p.is_file() else ""

    