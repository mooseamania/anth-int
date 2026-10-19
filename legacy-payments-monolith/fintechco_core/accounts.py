"""Customer accounts and balances."""
from fintechco_core import auth, db, utils


def open_account(user_id, kind="checking"):
    acct = {"id": utils.new_id("acct"), "user_id": user_id, "kind": kind, "balance_cents": 0}
    db.table("accounts").append(acct)
    return acct


def accounts_for_token(token):
    user_id = auth.user_for_token(token)
    return [a for a in db.table("accounts") if a["user_id"] == user_id]


def get(account_id):
    return next((a for a in db.table("accounts") if a["id"] == account_id), None)


def owner_contact(account_id):
    acct = get(account_id)
    return next((u for u in db.table("users") if u["id"] == acct["user_id"]), None)
