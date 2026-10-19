"""Double-entry ledger. Source of truth for money movement."""
from fintechco_core import accounts, db, utils


def post_entry(debit_acct, credit_acct, amount_cents, memo=""):
    d, c = accounts.get(debit_acct), accounts.get(credit_acct)
    if d["balance_cents"] < amount_cents:
        raise ValueError("insufficient funds")
    d["balance_cents"] -= amount_cents
    c["balance_cents"] += amount_cents
    entry = {
        "id": utils.new_id("le"),
        "debit": debit_acct,
        "credit": credit_acct,
        "amount_cents": amount_cents,
        "memo": memo,
        "ts": utils.now(),
    }
    db.table("ledger").append(entry)
    return entry


def entries_for(account_id, since_ts=0):
    return [e for e in db.table("ledger")
            if account_id in (e["debit"], e["credit"]) and e["ts"] >= since_ts]
