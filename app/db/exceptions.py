class PgError:
    TOO_LONG = "22001"
    UNIQUE = "23505"
    FK = "23503"
    NUMERIC = "22003"
    CHECK = "23514"
    CONVERT = "22P02"
    RAISE = "P0001"
    NOQUERY = "23502"
    NOENTITY = "42P01"
    NOPROC = "42883"
    WRONGTIME = "22007"


class DbError(Exception):
    pass


class TooLongError(DbError):
    pass


class UniqueError(DbError):
    pass


class FKError(DbError):
    pass


class NumericError(DbError):
    pass


class CheckError(DbError):
    pass


class ConvertError(DbError):
    pass


class UnknownError(DbError):
    pass


class EntityError(DbError):
    pass
