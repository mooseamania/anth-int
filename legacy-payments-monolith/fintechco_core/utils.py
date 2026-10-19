"""Misc helpers."""
import time
import uuid

from fintechco_core import config


def new_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def now():
    return int(time.time())


def cents(amount_str):
    return int(round(float(amount_str) * 100))


def within_daily_limit(total_cents):
    return total_cents <= config.DAILY_TRANSFER_LIMIT_CENTS
