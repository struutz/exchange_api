from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Transaction:
    amount: Decimal
    currency: str
    category: str
    date: datetime
    description: str
    id: Optional[int | None] = None