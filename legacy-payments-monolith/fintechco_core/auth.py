"""Authentication and sessions (used by web, mobile and batch)."""
import hashlib

from fintechco_core import config, db, utils


def login(username, password):
    users = db.table("users")
    digest = hashlib.sha256(password.encode()).hexdigest()
    for u in users:
        if u["username"] == username and u["pw"] == digest:
            token = utils.new_id("sess")
            db.table("sessions").append(
                {"token": token, "user_id": u["id"], "exp": utils.now() + config.SESSION_TTL_SECONDS}
            )
            return token
    return None


def user_for_token(token):
    for s in db.table("sessions"):
        if s["token"] == token and s["exp"] > utils.now():
            return s["user_id"]
    return None
