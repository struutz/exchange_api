from decimal import Decimal
from datetime import datetime
from app.domain.entities.transaction import Transaction


def test_create_transaction():
    transaction = Transaction(
        id=1,
        amount=Decimal("120.50"),
        currency="USD",
        category="Books",
        date=datetime(2025, 8, 4),
        description="Books from 2025, August"
    )

    assert transaction.id == 1
    assert transaction.amount == Decimal("120.50")
    assert transaction.date == datetime(2025, 8, 4)