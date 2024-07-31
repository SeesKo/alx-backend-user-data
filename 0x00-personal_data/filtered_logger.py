#!/usr/bin/env python3
"""
Filter log messages to obfuscate PII fields
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate the given fields in the log message.
    """
    pattern = '|'.join(f'{field}=.*?{separator}' for field in fields)
    return re.sub(
        pattern,
        lambda m: f'{m.group(0).split("=")[0]}={redaction}{separator}',
        message
    )
