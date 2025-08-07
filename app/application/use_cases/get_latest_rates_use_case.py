from typing import Optional, Dict, Any
from app.infrastructure.services.exchange_service import ExchangeService


class GetLatestRatesUseCase:
    def __init__(self, exchange_service: ExchangeService):
        self.service = exchange_service

    async def execute(self, symbols: Optional[str] = None) -> Optional[Dict[str, Any]]:
        result = await self.service.get_latest_rates(symbols=symbols)

        if result:
            return {
                "base": result.get("base"),
                "date": result.get("date"),
                "rates": result.get("rates")
            }

        return None
