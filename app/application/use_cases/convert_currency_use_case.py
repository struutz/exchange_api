from decimal import Decimal

from app.domain.services.exchange_service import ExchangeService


class ConvertCurrencyUseCase:
    def __init__(self, exchange_service: ExchangeService):
        self.service = exchange_service

    async def execute(
            self,
            from_currency: str,
            to_currency: str,
            amount: Decimal,
            to_currency_target: str) -> Decimal:

        return await self.service.convert(from_currency, to_currency, amount, to_currency_target)

