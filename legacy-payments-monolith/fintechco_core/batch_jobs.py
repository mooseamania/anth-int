"""Nightly jobs: settlement, statements, warehouse export."""
from fintechco_core import accounts, db, ledger, notifications, payments, reporting, utils


def nightly_settlement():
    day_start = utils.now() - 86400
    summary = reporting.daily_volume(day_start)
    for a in db.table("accounts"):
        if payments.recent_for_account(a["id"], window_s=86400):
            ledger.entries_for(a["id"], since_ts=day_start)
    return summary


def send_monthly_statements():
    for a in db.table("accounts"):
        stmt = reporting.account_statement(a["id"], since_ts=utils.now() - 86400 * 30)
        notifications.payment_sent(a["id"], stmt["balance_cents"])  # reuse of a template, sigh


def run_all():
    nightly_settlement()
    send_monthly_statements()
    return reporting.export_to_warehouse()
