from decimal import Decimal
from typing import Optional

import strawberry
from datetime import datetime


@strawberry.type(description="Transaction Type with value, currency and category of a financial transaction")
class TransactionType:
    id: Optional[int] = None
    amount: float
    currency: str
    category: str
    date: datetime
    description: str


@strawberry.type(description="Object Type with result of a financial conversion")
class ConversionResultType:
    result: Decimal