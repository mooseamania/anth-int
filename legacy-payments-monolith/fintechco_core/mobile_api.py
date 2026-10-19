"""Mobile backend endpoints. Ships on the monolith's monthly release train."""
from fintechco_core import accounts, auth, notifications, payments, reporting


def api_login(username, password):
    token = auth.login(username, password)
    return {"token": token} if token else {"error": "invalid credentials"}


def api_home(token):
    accts = accounts.accounts_for_token(token)
    return {"accounts": [
        {"id": a["id"], "balance_cents": a["balance_cents"],
         "activity": reporting.mobile_activity_summary(a["id"])} for a in accts]}


def api_send(token, from_acct, to_acct, amount_cents):
    if from_acct not in [a["id"] for a in accounts.accounts_for_token(token)]:
        return {"error": "forbidden"}
    return payments.send_payment(from_acct, to_acct, amount_cents)


def api_register_push(token, device_id):
    return notifications._send_push(auth.user_for_token(token), f"registered {device_id}")
