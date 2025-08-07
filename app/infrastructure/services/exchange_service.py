import logging
from decimal import Decimal
from typing import Optional, Dict, Any
from app.infrastructure.logs.logger import logger
from decouple import config

import httpx


class ExchangeService:
    BASE_URL = "https://api.exchangeratesapi.io/v1"

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.API_KEY = api_key or config("EXCHANGE_API_KEY")
        self.LATEST_URL = f"{self.BASE_URL}/latest"

    async def convert(self, from_currency: str, to_currency: str, amount: Decimal) -> Optional[Decimal]:
        params = {
            "access_key": self.API_KEY,
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                logger.info("Received response from ExchangeratesAPI", extra={"response": data})

                if "result" in data:
                    return data["result"]

                logging.warning(f"Exchange API returned no result: {data}")
                return None
            except httpx.RequestError as e:
                logger.error("Request error during currency conversion", extra={"error_message": str(e), "params": params})
            except httpx.HTTPError as e:
                logger.error("HTTP error during currency conversion", extra={
                    "status_code": e.response.status_code,
                    "error_message": str(e),
                    "params": params
                })
            except Exception as e:
                logger.exception("Unexpected error during currency conversion", extra={"params": params})

        return None

    async def get_latest_rates(self, symbols: Optional[str] = None, format_response: bool = True) -> Optional[Dict[str, Any]]:
        params = {
            "access_key": self.API_KEY,
            "format": int(format_response)
        }

        if symbols:
            params["symbols"] = symbols

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.LATEST_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                logger.info("Received latest rates", extra={"response": data})

                if data.get("success") and "rates" in data:
                    return {
                        "base": data.get("base"),
                        "date": data.get("date"),
                        "rates": data.get("rates", {})
                    }

                logger.warning("Exchange API returned no rates", extra={"response": data})
                return None
            except httpx.RequestError as e:
                logger.error("Request error while fetching rates", extra={"error_message": str(e), "params": params})
            except httpx.HTTPError as e:
                logger.error("HTTP error while fetching rates", extra={"error_message": str(e), "params": params})
            except Exception as e:
                logger.exception("Unexpected error while fetching latest rates", extra={"params": params})

        return None
