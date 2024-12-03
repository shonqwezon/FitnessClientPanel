from enum import StrEnum
from os import getenv

MIN_CONN = 1
MAX_CONN = 10

db_params = {
    "dbname": getenv("DB_NAME"),
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_HOST"),
    "port": getenv("DB_PORT"),
}

db_params_su = {
    "dbname": getenv("DB_NAME"),
    "user": "postgres",
    "password": getenv("DB_PASSWORD_SU"),
    "host": getenv("DB_HOST"),
    "port": getenv("DB_PORT"),
}


class DbTable(StrEnum):
    MANAGER = "manager"
    SERVICE = "service"
    SPORTCENTER = "sportcenter"
    CLIENT = "client"
    PLAN = "plan"


class DbCmd:
    CREATE = "CREATE"
    DROP = "DROP"
