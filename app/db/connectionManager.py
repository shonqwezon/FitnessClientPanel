from contextlib import contextmanager
from typing import Any, Generator

import psycopg2.pool
from psycopg2.extensions import connection

from app import setup_logger

from . import config as cfg
from .exceptions import DbError

logger = setup_logger(__name__)


class ConnectionManager:
    def __init__(self, params: dict, autocommit=False):
        logger.info(f"Init connection pool with autocommit = {autocommit}")
        self.autocommit = autocommit
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(cfg.MIN_CONN, cfg.MAX_CONN, **params)
        except Exception as e:
            logger.error(f"Can't create connection to db:\n{e}")
            raise

    @contextmanager
    def get_connection(self) -> Generator[Any | connection, Any, None]:
        conn: connection = None
        try:
            conn = self.pool.getconn()
            conn.autocommit = self.autocommit
            yield conn
        except DbError:
            raise
        except Exception as e:
            logger.error(f"Error can't get connection:\n{e}")
            raise
        finally:
            if conn:
                self.pool.putconn(conn)

    def free(self):
        logger.info("Free connection pool")
        if not self.pool.closed:
            self.pool.closeall()
