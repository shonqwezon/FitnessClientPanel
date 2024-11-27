import psycopg2
from psycopg2 import sql

from app import setup_logger

from .connectionManager import ConnectionManager

logger = setup_logger(__name__)


class Database:
    def __init__(self):
        logger.info("Init db")
        self._pool = ConnectionManager()

    def close(self):
        logger.info("Close db")
        self._pool.free()
