"""Email + push notifications."""
from fintechco_core import accounts, config


def _send_email(to, subject, body):
    return {"via": config.SMTP_HOST, "to": to, "subject": subject}


def _send_push(user_id, body):
    return {"via": config.PUSH_GATEWAY, "user": user_id, "body": body}


def payment_sent(account_id, amount_cents):
    owner = accounts.owner_contact(account_id)
    _send_email(owner["email"], "Payment sent", f"${amount_cents/100:.2f} sent")
    return _send_push(owner["id"], "Payment sent")


def payment_blocked(account_id):
    owner = accounts.owner_contact(account_id)
    return _send_push(owner["id"], "We blocked a suspicious payment")
