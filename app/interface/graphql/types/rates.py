import strawberry
from typing import List


@strawberry.type
class Rate:
    currency: str
    value: float

@strawberry.type
class RatesResponseType:
    base: str
    date: str
    rates: List[Rate]