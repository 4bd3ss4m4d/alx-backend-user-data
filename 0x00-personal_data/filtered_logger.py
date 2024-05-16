#!/usr/bin/env python3

'''
This module contains the following:
- filter_datum
- RedactingFormatter
- get_logger
- get_db
- main
'''

import re
import logging
import os
import mysql.connector
from typing import List



def filter_datum(
    fields: List[str], redaction: str, final_msg: str, separator: str
) -> str:
    '''
    Returns a string.
    
    Args:
        fields: a list of strings.
        redaction: a string argument.
        message: a string argument.
        separator: a string argument.
    
    Returns:
        A string.
    '''
    for fie in fields:
        pattern = f"{fie}=[^{separator}]*"
        final_msg = re.sub(pattern, f"{fie}={redaction}", final_msg)
    return final_msg


class RedactingFormatter(logging.Formatter):
    '''
    RedactingFormatter class.
    
    Attributes:
        REDACTION: a string.
        FORMAT: a string.
        SEPARATOR: a string.
    
    Methods:
        format: Returns a string.
    '''

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''
        Initializes the RedactingFormatter object.
        
        Args:
            fields: a list of strings.
        
        Returns:
            None.
        '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        Returns a string.
        
        Args:
            record: a logging.LogRecord object.
        
        Returns:
            A string.
        '''
        record_org = super().format(record)
        return filter_datum(self.fields, self.REDACTION, record_org, self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    '''
    Returns a logging.Logger object.
    
    Args:
        None.
    
    Returns:
        A logging.Logger object.
    '''
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(sh)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    Returns a MySQLConnection object.

    Args:
        None.
    '''
    uname = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    psswd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=uname, password=psswd, host=host, database=db_name
    )


def main() -> None:
    '''
    Main function.
    '''
    database = get_db()
    crsr = database.cursor()
    crsr.execute("SELECT * FROM users;")
    log = get_logger()
    for element in crsr:
        dt = []
        for desc, value in zip(crsr.description, element):
            pair = f"{desc[0]}={str(value)}"
            dt.append(pair)
        row_str = "; ".join(dt)
        log.info(row_str)
    crsr.close()
    database.close()


if __name__ == "__main__":
    main()
