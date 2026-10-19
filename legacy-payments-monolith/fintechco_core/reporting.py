"""Reporting / BI extracts. Reads directly across ledger, payments and accounts tables."""
from fintechco_core import accounts, config, db, ledger, payments


def daily_volume(day_start_ts):
    rows = [p for p in db.table("payments") if day_start_ts <= p["ts"] < day_start_ts + 86400]
    return {"count": len(rows), "cents": sum(p["amount_cents"] for p in rows)}


def account_statement(account_id, since_ts=0):
    acct = accounts.get(account_id)
    return {"account": acct["id"], "balance_cents": acct["balance_cents"],
            "entries": ledger.entries_for(account_id, since_ts)}


def export_to_warehouse():
    snapshot = {"payments": list(db.table("payments")), "ledger": list(db.table("ledger"))}
    return {"target": config.REPORT_WAREHOUSE_URL, "rows": sum(len(v) for v in snapshot.values())}


def mobile_activity_summary(account_id):
    recent = payments.recent_for_account(account_id, window_s=86400 * 30)
    return {"payments_30d": len(recent), "volume_cents_30d": sum(p["amount_cents"] for p in recent)}
