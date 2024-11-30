from pathlib import Path

import psycopg2
from psycopg2 import sql

from app import setup_logger

from .connectionManager import ConnectionManager

logger = setup_logger(__name__)


class Database:
    def __init__(self):
        logger.info("Init db")
        self.pool = ConnectionManager()
        self.create_tables()

    def create_tables(self):
        tables = [file for file in Path("app/db/scripts/tables").iterdir() if file.is_file()]
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                for table in tables:
                    logger.debug(f"Creating {table}...")
                    with open(table, "r", encoding="utf-8") as sql_file:
                        cursor.execute(sql_file.read())
                logger.debug("Adding constraints to tables...")
                with open("app/db/scripts/constraints.sql", "r", encoding="utf-8") as sql_file:
                    cursor.execute(sql_file.read())
            conn.commit()

    def close(self):
        logger.info("Close db")
        self.pool.free()
