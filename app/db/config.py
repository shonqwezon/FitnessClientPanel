from enum import StrEnum
from os import getenv

MIN_CONN = 1
MAX_CONN = 10

db_params = {
    "dbname": "fitness_db",
    "user": "fitness_user",
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_HOST"),
    "port": getenv("DB_PORT"),
}

db_params_su = {
    "dbname": "fitness_db",
    "user": getenv("DB_USER_SU"),
    "password": getenv("DB_PASSWORD_SU"),
    "host": getenv("DB_HOST"),
    "port": getenv("DB_PORT"),
}


class DbTable(StrEnum):
    MANAGER = "manager"
    SERVICE = "service"
    SPORTCENTER = "sportcenter"
    CLIENT = "client"
    CLIENT_PLAN = "client_plan"
    PLAN = "plan"
    PLAN_TECH = "plan_tech"
