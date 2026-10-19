"""Payment orchestration: limits -> fraud -> ledger -> notify."""
from fintechco_core import accounts, config, db, fraud, ledger, notifications, utils


def send_payment(from_acct, to_acct, amount_cents):
    today = [p for p in recent_for_account(from_acct, window_s=86400)]
    if not utils.within_daily_limit(sum(p["amount_cents"] for p in today) + amount_cents):
        raise ValueError("daily limit exceeded")

    s = fraud.score(from_acct, amount_cents)
    if fraud.should_block(s):
        notifications.payment_blocked(from_acct)
        return {"status": "blocked", "score": s}

    entry = ledger.post_entry(from_acct, to_acct, amount_cents, memo="p2p")
    pay = {"id": utils.new_id("pay"), "from": from_acct, "to": to_acct,
           "amount_cents": amount_cents, "ledger_id": entry["id"], "ts": utils.now()}
    db.table("payments").append(pay)
    notifications.payment_sent(from_acct, amount_cents)
    return {"status": "sent", "payment_id": pay["id"]}


def recent_for_account(account_id, window_s):
    cutoff = utils.now() - window_s
    return [p for p in db.table("payments") if p["from"] == account_id and p["ts"] >= cutoff]
