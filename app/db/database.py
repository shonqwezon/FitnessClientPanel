from datetime import date, time
from os import getenv
from pathlib import Path
from typing import Any

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection

from app import setup_logger

from .config import DbTable, db_params, db_params_su
from .connectionManager import ConnectionManager
from .exceptions import (
    CheckError,
    ConvertError,
    EntityError,
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
        self.create_schema()
        self.create_tables()
        self.pool = ConnectionManager(db_params, True)

    def drop_db(self):
        self.close()
        self.pool_su = ConnectionManager(db_params_su)
        with self.pool_su.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("call init.drop_db()")
                    conn.commit()
            except Exception as e:
                logger.error(e)

    def drop_table(self, table_name: DbTable = None):
        logger.debug(f"drop_table {table_name}")
        with self.pool.get_connection() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                try:
                    if table_name:
                        cursor.execute("call app.drop_table(%s)", (table_name,))
                    else:
                        cursor.execute("call app.drop_tables()")
                except Exception as e:
                    logger.error(e.pgerror)
                    if e.pgcode == PgError.NOENTITY:
                        raise EntityError(f"Таблицы {table_name} не существует")
                    else:
                        raise UnknownError()

    def create_schema(self):
        logger.debug("Setting up schema...")
        self.pool_su = ConnectionManager(db_params_su)
        with self.pool_su.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("call init.setup_schema(%s)", (db_params["password"],))
                    conn.commit()
            except Exception as e:
                logger.error(e)

    def create_tables(self):
        logger.debug("create_tables")
        with self.pool_su.get_connection() as conn:
            with conn.cursor() as cursor:
                # Init tables
                cursor.execute("call init.create_tables()")
                # Init constraints
                logger.debug("Adding constraints to tables...")
                cursor.execute("call init.add_constraints()")
            conn.commit()

    def is_admin(self, login: str, password: str) -> bool:
        return (
            getenv("ADMIN_LOGIN") == login.strip() and getenv("ADMIN_PASSWORD") == password.strip()
        )

    def close(self):
        logger.info("Close db")
        self.pool.free()
        self.pool_su.free()

    def get_table(self, table_name: DbTable, id_parameter: Any = None):
        logger.debug(f"get_table {table_name}")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    req = f"get_{table_name}"
                    if id_parameter:
                        cursor.callproc(req, [id_parameter])
                        res = cursor.fetchall()
                    else:
                        cursor.callproc(req)
                        res = cursor.fetchall()
                    return res
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.RAISE:
                            raise FKError(f"Указанного {table_name} не существует")
                        case PgError.CONVERT:
                            raise ConvertError(f"Неверный формат {table_name}_id, ожидалось число")
                        case _:
                            raise UnknownError()

    # Client

    def add_client(self, fullname: str, balance: int):
        logger.debug("add_client")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call add_client(%s, %s)", (fullname, balance))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.TOO_LONG:
                            raise TooLongError("Слишком длинное ФИО")
                        case PgError.UNIQUE:
                            raise UniqueError("Такой клиент уже зарегистрирован")
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат баланса")
                        case PgError.CHECK:
                            raise CheckError("Проверьте баланс и/или Имя клиента")
                        case PgError.NUMERIC:
                            raise NumericError("Ожидался new_balance с точностью 8, порядка 2")
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
                            raise FKError("Указанного клиента не существует")
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
                        case (
                            PgError.ARIFMETIC
                            | PgError.WRONGTIME
                            | PgError.NUMERIC
                            | PgError.DATETIME
                        ):
                            raise CheckError("Выбрана некорректная дата окончания тарифа")
                        case PgError.CHECK:
                            raise CheckError(
                                "У клиента недостаточно средств или некорректный plan_end"
                            )
                        case PgError.UNIQUE:
                            raise UniqueError("Клиент уже имеет данный тариф")
                        case _:
                            raise UnknownError()

    def change_client_plan(
        self, client_id: int, plan_id: int, plan_end: date, new_client_id: int = None
    ):
        logger.debug("change_client_plan")
        with self.pool.get_connection() as conn:
            conn.autocommit = False
            with conn.cursor() as cursor:
                try:
                    cursor.callproc("delete_client_plan", [client_id])
                    if new_client_id:
                        client_id = new_client_id
                    cursor.execute("call set_plan(%s, %s, %s)", (client_id, plan_id, plan_end))
                    conn.commit()
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.RAISE:
                            raise FKError("Указанного клиента или плана не существует")
                        case PgError.CONVERT:
                            raise ConvertError(
                                "Неверный формат client_id или plan_id, ожидалось число"
                            )
                        case (
                            PgError.ARIFMETIC
                            | PgError.WRONGTIME
                            | PgError.NUMERIC
                            | PgError.DATETIME
                        ):
                            raise CheckError("Выбрана некорректная дата окончания тарифа")
                        case PgError.NOQUERY | PgError.FK:
                            raise FKError(
                                "Указанного клиента или спортивного центра не существует"
                            )
                        case PgError.CHECK:
                            raise CheckError(
                                "У клиента недостаточно средств или некорректный plan_end"
                            )
                        case PgError.UNIQUE:
                            raise UniqueError("Клиент уже имеет данный тариф")
                        case _:
                            raise UnknownError()

    # Manager

    def is_correct_manager(self, email: str, password_hash: str) -> bool:
        logger.debug("is_correct_manager")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.callproc("is_correct_manager", [email, password_hash])
                    return cursor.fetchone()[0]
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case _:
                            raise UnknownError()

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

    def delete_manager(self, fullname: str):
        logger.debug("delete_manager")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call delete_manager(%s)", (fullname,))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.RAISE:
                            raise FKError("Указанного менеджера не существует")
                        case PgError.NOPROC:
                            raise ConvertError("Неверный формат fullname, ожидалась строка")
                        case _:
                            raise UnknownError()

    # Sportcenter

    def add_sportcenter(
        self, name: str, address: str, open_time: time, close_time: time, cost_ratio: float
    ):
        logger.debug("add_sportcenter")
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
                            raise UniqueError(
                                f"Спортивный центр с name={name} центр уже сущуствует"
                            )
                        case PgError.NUMERIC:
                            raise NumericError("Ожидалось cost_ratio с точностью 3, порядка 2")
                        case PgError.CHECK:
                            raise CheckError("Нарушено ограничение таблицы")
                        case PgError.CONVERT | PgError.WRONGTIME | PgError.DATETIME:
                            raise ConvertError("Неверный формат данных (времени или числа)")
                        case _:
                            raise UnknownError()

    def delete_sportcenter(self, sportcenter_id: int):
        logger.debug("delete_sportcenter")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call delete_sportcenter(%s)", (sportcenter_id,))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.RAISE:
                            raise FKError("Указанного спортивного центра не существует")
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат sportcenter_id, ожидалось число")
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

    def delete_service(self, service_id: int):
        logger.debug("delete_service")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call delete_service(%s)", (service_id,))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.RAISE:
                            raise FKError("Указанной услуги не существует")
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат service_id, ожидалось число")
                        case _:
                            raise UnknownError()

    # Plan

    def add_plan(
        self,
        name: str,
        base_cost: int,
        begin_time: time,
        end_time: time,
        sportcenter_id: int,
        service_ids: list[int],
    ):
        logger.debug("add_plan")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "call add_plan(%s, %s, %s, %s, %s, %s)",
                        (name, base_cost, begin_time, end_time, sportcenter_id, service_ids),
                    )
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.TOO_LONG:
                            raise TooLongError("Слишком длинное название тарифа")
                        case PgError.UNIQUE:
                            raise UniqueError(f"Тариф с названием '{name}' уже сущуствует")
                        case PgError.FK:
                            raise FKError("Указанные id услуг не существуют")
                        case PgError.CHECK:
                            raise CheckError("Нарушено ограничение таблицы")
                        case PgError.CONVERT | PgError.WRONGTIME | PgError.DATETIME:
                            raise ConvertError("Неверный формат данных (времени или id)")
                        case PgError.RAISE:
                            raise CheckError(
                                "Временные рамки плана \
не должны выходить за рабочие часы спортивного центра"
                            )
                        case _:
                            raise UnknownError()

    def delete_plan(self, plan_id: int):
        logger.debug("delete_plan")
        with self.pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("call delete_plan(%s)", (plan_id,))
                except Exception as e:
                    logger.error(e.pgerror)
                    match e.pgcode:
                        case PgError.RAISE:
                            raise FKError("Указанного плана не существует")
                        case PgError.CONVERT:
                            raise ConvertError("Неверный формат plan_id, ожидалось число")
                        case _:
                            raise UnknownError()
