from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional


class ExchangeService(ABC):
    @abstractmethod
    async def convert(self,
                      from_currency: str,
                      to_currency: str,
                      amount: Decimal,
                      to_currency_target: str) -> Optional[Decimal]:
        pass