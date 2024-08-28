#!/usr/bin/env python3
"""Module for filtering sensitive information from log messages."""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    pattern = '|'.join([f'{field}=[^\\{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)
