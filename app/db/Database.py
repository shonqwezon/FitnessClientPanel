from datetime import date, time
from os import getenv
from pathlib import Path

import psycopg2
from psycopg2 import sql

from app import setup_logger

from .config import DB_CMD, db_params, db_params_su
from .connectionManager import ConnectionManager
from .exceptions import (
    CheckError,
    ConvertError,
    FKError,
    NumericError,
    PgError,
    TooLongError,
    UniqueError,
    UnknownError,
)

logger = setup_logger(__name__)


class Database:
    def __init__(self):
        logger.info("Init db")
        self.create_db()
        self.create_tables()
        self.create_triggers()
        self.create_procedures()
        self.pool = ConnectionManager(db_params, True)

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

    # Client

    def add_client(self, fullname: str):
        logger.debug("add_client")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call add_client(%s)", (fullname,))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.TOO_LONG:
                            raise TooLongError("Слишком длинное ФИО")
                        case PgError.UNIQUE:
                            raise UniqueError("Такое ФИО уже было зарегистрировано")
                        case _:
                            raise UnknownError()

    def update_balance(self, client_id: int, new_balance: int):
        logger.debug("update_balance")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call update_client_balance(%s, %s)", (client_id, new_balance))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.NOQUERY | PgError.RAISE:
                            raise FKError(
                                "Указанного клиента или спортивного центра не существует"
                            )
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат данных (времени или числа)")
                        case PgError.CHECK:
                            raise CheckError("Баланс не может быть отрицательным")
                        case PgError.NUMERIC:
                            raise NumericError("Ожидался new_balance с точностью 8, порядка 2")
                        case _:
                            raise UnknownError()

    def set_client_plan(self, client_id: int, plan_id: int, plan_end: date):
        logger.debug("set_client_plan")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call set_plan(%s, %s, %s)", (client_id, plan_id, plan_end))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.NOQUERY | PgError.FK:
                            raise FKError(
                                "Указанного клиента или спортивного центра не существует"
                            )
                        case PgError.CHECK:
                            raise CheckError(
                                "У клиента недостаточно средств или некорректный plan_end"
                            )
                        case _:
                            raise UnknownError()

    def delete_client_plan(self, client_id: int, plan_id: int) -> date:
        logger.debug("delete_client_plan")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.callproc("delete_client_plan", [client_id, plan_id])
                    return cursor.fetchone()[0]
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.RAISE:
                            raise FKError("Указанного клиента или плана не существует")
                        case PgError.CONVERT:
                            raise ConvertError(
                                "Неверный формат client_id или plan_id, ожидалось число"
                            )
                        case _:
                            raise UnknownError()

    # Manager

    def add_manager(self, fullname: str, email: str, password_hash: str, sportcenter_id: int):
        logger.debug("add_manager")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "call add_manager(%s, %s, %s, %s)",
                        (
                            fullname,
                            email,
                            password_hash,
                            sportcenter_id,
                        ),
                    )
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.TOO_LONG:
                            raise TooLongError("Слишком длинное ФИО")
                        case PgError.UNIQUE:
                            raise UniqueError("Такое ФИО уже было зарегистрировано")
                        case PgError.FK:
                            raise FKError(
                                f"Спортивного центра с id={sportcenter_id} не существует"
                            )
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат sportcenter_id, ожидалось число")
                        case _:
                            raise UnknownError()

    # Sportcenter

    def add_sportcenter(
        self, name: str, address: str, open_time: time, close_time: time, cost_ratio: float
    ):
        logger.debug("add_client")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "call add_sportcenter(%s, %s, %s, %s, %s)",
                        (name, address, open_time, close_time, cost_ratio),
                    )
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.TOO_LONG:
                            raise TooLongError("Слишком длинное название центра или его адреса")
                        case PgError.UNIQUE:
                            raise UniqueError(f"Спортивный с name={name} центр уже сущуствует")
                        case PgError.NUMERIC:
                            raise NumericError("Ожидалось cost_ratio с точностью 3, порядка 2")
                        case PgError.CHECK:
                            raise CheckError("Нарушено ограничение таблицы")
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат данных (времени или числа)")
                        case _:
                            raise UnknownError()

    # Service

    def add_service(self, description: str, cost: int):
        logger.debug("add_service")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call add_service(%s, %s)", (description, cost))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.TOO_LONG:
                            raise TooLongError("Слишком длинное название центра или его адреса")
                        case PgError.UNIQUE:
                            raise UniqueError(f"Услуга с description={description} уже сущуствует")
                        case PgError.NUMERIC:
                            raise NumericError("Ожидалось cost_ratio с точностью 5, порядка 2")
                        case PgError.CHECK:
                            raise CheckError("Нарушено ограничение таблицы")
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат cost, ожидалось число")
                        case _:
                            raise UnknownError()

    # Plan

    def add_plan(self, base_cost: int, begin_time: time, end_time: time, sportcenter_id: int):
        logger.debug("add_plan")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "call add_plan(%s, %s, %s, %s)",
                        (base_cost, begin_time, end_time, sportcenter_id),
                    )
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.CHECK:
                            raise CheckError("Нарушено ограничение таблицы")
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат данных (времени или id)")
                        case PgError.RAISE:
                            raise CheckError(
                                "Временные рамки плана\
не должны выходить за рабочие часы спортивного центра"
                            )
                        case _:
                            raise UnknownError()
