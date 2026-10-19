"""Global settings. Imported by nearly everything (classic monolith smell)."""
import os

DB_URL = os.environ.get("CORE_DB_URL", "postgresql://core:core@localhost/core")
FRAUD_SCORE_BLOCK_THRESHOLD = 0.85
DAILY_TRANSFER_LIMIT_CENTS = 2_500_000
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.internal")
PUSH_GATEWAY = os.environ.get("PUSH_GATEWAY", "https://push.internal")
SESSION_TTL_SECONDS = 3600
REPORT_WAREHOUSE_URL = os.environ.get("WAREHOUSE_URL", "redshift://bi.internal/prod")
