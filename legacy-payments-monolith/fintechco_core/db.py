"""Single shared connection used by every module."""
from fintechco_core import config

_conn = None


def get_conn():
    global _conn
    if _conn is None:
        _conn = {"url": config.DB_URL, "tables": {}}
    return _conn


def table(name):
    return get_conn()["tables"].setdefault(name, [])
