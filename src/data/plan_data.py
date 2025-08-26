"""
Plan data
"""

from decimal import Decimal

from database.models.plan import Plan

plans = [
    Plan(
        name="free",
        token_limit_daily=10000,
        document_limit=5,
        session_limit=3,
        price_monthly=Decimal("0.00"),
        is_active=True,
    ),
    Plan(
        name="pro",
        token_limit_daily=100000,
        document_limit=50,
        session_limit=25,
        price_monthly=Decimal("19.99"),
        is_active=True,
    ),
    Plan(
        name="enterprise",
        token_limit_daily=1000000,
        document_limit=500,
        session_limit=100,
        price_monthly=Decimal("99.99"),
        is_active=True,
    ),
]
