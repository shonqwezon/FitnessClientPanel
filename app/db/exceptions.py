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


class TooLongError(Exception):
    pass


class UniqueError(Exception):
    pass


class FKError(Exception):
    pass


class NumericError(Exception):
    pass


class CheckError(Exception):
    pass


class ConvertError(Exception):
    pass


class UnknownError(Exception):
    pass


class EntityError(Exception):
    pass
