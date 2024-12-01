from os import getenv
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
        self.create_triggers()
        self.create_procedures()

    def create_tables(self):
        logger.debug("create_tables")
        tables = [file for file in Path("app/db/scripts/tables").iterdir() if file.is_file()]
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                # Init tables
                for table in tables:
                    logger.debug(f"Creating {table}...")
                    with open(table, "r", encoding="utf-8") as sql_file:
                        cursor.execute(sql_file.read())
                # Init constraints
                logger.debug("Adding constraints to tables...")
                with open("app/db/scripts/constraints.sql", "r", encoding="utf-8") as sql_file:
                    cursor.execute(sql_file.read())
            conn.commit()

    def create_triggers(self):
        logger.debug("create_triggers")
        triggers = [file for file in Path("app/db/scripts/triggers").iterdir() if file.is_file()]
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                for trigger in triggers:
                    logger.debug(f"Creating {trigger}...")
                    with open(trigger, "r", encoding="utf-8") as sql_file:
                        cursor.execute(sql_file.read())
            conn.commit()

    def create_procedures(self):
        logger.debug("create_procedures")
        folder_path = Path("app/db/scripts/procedures")
        procedures = [file for file in list(folder_path.rglob("*")) if file.is_file()]
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                for proc in procedures:
                    logger.debug(f"Creating {proc}...")
                    with open(proc, "r", encoding="utf-8") as sql_file:
                        cursor.execute(sql_file.read())
            conn.commit()

    def is_admin(login: str, password: str):
        return (
            getenv("ADMIN_LOGIN") == login.strip() and getenv("ADMIN_PASSWORD") == password.strip()
        )

    def close(self):
        logger.info("Close db")
        self.pool.free()
