
import pytest
import respx
from httpx import Response
from decimal import Decimal
from app.infrastructure.services.exchange_service import ExchangeService


@pytest.mark.asyncio
@respx.mock
async def test_convert_success():
    expected_result = 123.45
    respx.get("https://api.exchangeratesapi.io/v1", params={
        "access_key": "test_key",
        "from": "USD",
        "to": "EUR",
        "amount": Decimal("100")
    }).mock(return_value=Response(200, json={"result": expected_result}))

    service = ExchangeService(api_key="test_key")
    result = await service.convert("USD", "EUR", Decimal("100"))

    assert result == expected_result


@pytest.mark.asyncio
@respx.mock
async def test_convert_request_error(caplog):
    respx.get("https://api.exchangeratesapi.io/v1").mock(side_effect=Exception("Connection error"))

    service = ExchangeService(api_key="test_key")
    result = await service.convert("USD", "EUR", Decimal("100"))

    assert result is None
    assert any("Unexpected error during currency conversion" in record.message for record in caplog.records)


@pytest.mark.asyncio
@respx.mock
async def test_convert_no_result():
    respx.get("https://api.exchangeratesapi.io/v1").mock(return_value=Response(200, json={"success": False}))

    service = ExchangeService(api_key="test_key")
    result = await service.convert("USD", "EUR", Decimal("100"))

    assert result is None


@pytest.mark.asyncio
@respx.mock
async def test_get_latest_rates_success():
    expected_response = {
        "base": "USD",
        "date": "2025-01-01",
        "rates": {"EUR": 0.9},
        "success": True
    }

    respx.get("https://api.exchangeratesapi.io/v1/latest", params={
        "access_key": "test_key",
        "format": 1
    }).mock(return_value=Response(200, json=expected_response))

    service = ExchangeService(api_key="test_key")
    result = await service.get_latest_rates()

    assert result == {
        "base": "USD",
        "date": "2025-01-01",
        "rates": {"EUR": 0.9}
    }


@pytest.mark.asyncio
@respx.mock
async def test_get_latest_rates_no_rates():
    respx.get("https://api.exchangeratesapi.io/v1/latest").mock(return_value=Response(200, json={"success": False}))

    service = ExchangeService(api_key="test_key")
    result = await service.get_latest_rates()

    assert result is None


@pytest.mark.asyncio
@respx.mock
async def test_get_latest_rates_request_error(caplog):
    respx.get("https://api.exchangeratesapi.io/v1/latest").mock(side_effect=Exception("Request timeout"))

    service = ExchangeService(api_key="test_key")
    result = await service.get_latest_rates()

    assert result is None
    assert any("Unexpected error while fetching latest rates" in record.message for record in caplog.records)
