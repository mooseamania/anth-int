"""Fraud scoring. NOTE: circular dependency with payments (known debt)."""
from fintechco_core import config, db, ledger, payments, utils


def score(account_id, amount_cents):
    recent = payments.recent_for_account(account_id, window_s=3600)  # <- cycle
    velocity = len(recent)
    history = ledger.entries_for(account_id, since_ts=utils.now() - 86400 * 30)
    avg = (sum(e["amount_cents"] for e in history) / len(history)) if history else amount_cents
    s = min(1.0, 0.1 * velocity + (0.5 if amount_cents > 5 * avg else 0.0))
    db.table("fraud_scores").append({"account": account_id, "score": s, "ts": utils.now()})
    return s


def should_block(score_value):
    return score_value >= config.FRAUD_SCORE_BLOCK_THRESHOLD
