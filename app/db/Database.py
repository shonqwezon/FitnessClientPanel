from os import getenv
from pathlib import Path

import psycopg2
from psycopg2 import sql

from app import setup_logger

from .config import DB_CMD, db_params, db_params_su
from .connectionManager import ConnectionManager

logger = setup_logger(__name__)


class Database:
    def __init__(self):
        logger.info("Init db")
        self.create_db()
        self.create_tables()
        self.create_triggers()
        self.create_procedures()
        self.pool = ConnectionManager(db_params)
        # self.drop_db()

    def drop_db(self):
        self.close()
        self.db(DB_CMD.DROP)

    def create_db(self):
        self.db(DB_CMD.CREATE)
        logger.debug("Db has been created, now it is setting up...")
        self.pool_su = ConnectionManager(db_params_su)
        with self.pool_su.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    with open("app/db/scripts/setup_db.sql", "r", encoding="utf-8") as sql_file:
                        cursor.execute(
                            sql_file.read().format(
                                user=db_params["user"],
                                password=db_params["password"],
                            )
                        )

                    conn.commit()
            except Exception as e:
                logger.error(e)

    def db(self, cmd: str):
        query = sql.SQL("{0} DATABASE {1}").format(
            sql.SQL(cmd), sql.Identifier(db_params["dbname"])
        )
        logger.debug(query)
        try:
            t_db_params_su = db_params_su.copy()
            t_db_params_su["dbname"] = "postgres"
            conn = psycopg2.connect(**t_db_params_su)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(query)
            if cmd == DB_CMD.DROP:
                cursor.execute(sql.SQL("DROP USER {0}").format(sql.SQL(db_params["user"])))
        except Exception as e:
            logger.error(f"Cannot {cmd} db: {e}")
        finally:
            conn.close()

    def create_tables(self):
        logger.debug("create_tables")
        tables = [file for file in Path("app/db/scripts/tables").iterdir() if file.is_file()]
        with self.pool_su.get_connection() as conn:
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
        with self.pool_su.get_connection() as conn:
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
        with self.pool_su.get_connection() as conn:
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
        self.pool_su.free()
