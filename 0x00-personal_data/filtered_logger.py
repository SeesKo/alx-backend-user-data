#!/usr/bin/env python3
"""
Filter log messages to obfuscate PII fields
and connect to a secure database
"""

import logging
import mysql.connector
import os
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str,
    message: str, separator: str
) -> str:
    """
    Obfuscate the given fields in the log message.
    """
    pattern = '|'.join(f'{field}=.*?{separator}' for field in fields)
    return re.sub(
        pattern,
        lambda m: f'{m.group(0).split("=")[0]}={redaction}{separator}',
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize RedactingFormatter with fields to be redacted.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by redacting specified fields.
        """
        return filter_datum(
            self.fields, self.REDACTION,
            super().format(record), self.SEPARATOR
        )


# Define PII_FIELDS from user_data.csv
PII_FIELDS = (
    "name", "email", "phone",
    "ssn", "password"
)


def get_logger() -> logging.Logger:
    """
    Get a configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Do not propagate to other loggers

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Get a database connection using credentials from environment variables.
    """
    # Retrieve environment variables with default values
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Check if the database name is provided
    if not db_name:
        raise ValueError("Database name must be set.")

    # Create a connection to the MySQL database
    connection = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return connection


def main() -> None:
    """
    Main function to fetch and display user data with filtered PII.
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        # Construct log message
        message = "; ".join(f"{key}={value}" for key, value in row.items())
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
