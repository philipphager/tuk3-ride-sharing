import logging
import os
import socket

import pyhdb

from database.const import DB_SCHEMA
from error.DatabaseNotConnected import DatabaseConnectionError


class HanaConnection(object):
    def __init__(self):
        hana_user = os.environ.get('HANA_USER')
        hana_pwd = os.environ.get('HANA_PWD')
        if not hana_pwd and not hana_user:
            raise EnvironmentError('Please provide user and password as environment variables (HANA_USER, HANA_PWD)!')
        try:
            self.connection = pyhdb.Connection(
                host="side.eaalab.hpi.uni-potsdam.de",
                port=30015,
                user=hana_user,
                password=hana_pwd,
                autocommit=True,
                timeout=None
            )
            self.connection.connect()
            self.cursor = self.connection.cursor()
            self.cursor.execute('SET SCHEMA {}'.format(DB_SCHEMA))
        except socket.gaierror as e:
            logging.error('Database instance is not available!')
            raise DatabaseConnectionError(message='Database instance is not available!')

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logging.error(exc_type, exc_value, traceback)
        self.cursor.close()
        self.connection.close()
