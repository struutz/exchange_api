import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.get_latest_rates_use_case import GetLatestRatesUseCase


@pytest.fixture
def mock_exchange_service():
    return AsyncMock()


@pytest.mark.asyncio
async def test_execute_returns_formatted_result(mock_exchange_service):
    expected_response = {
        "base": "USD",
        "date": "2025-08-07",
        "rates": {
            "EUR": 0.92,
            "BRL": 5.30
        }
    }

    mock_exchange_service.get_latest_rates.return_value = expected_response

    use_case = GetLatestRatesUseCase(mock_exchange_service)

    result = await use_case.execute("EUR,BRL")

    assert result == expected_response
    mock_exchange_service.get_latest_rates.assert_awaited_once_with(symbols="EUR,BRL")


@pytest.mark.asyncio
async def test_execute_returns_none_when_service_returns_none(mock_exchange_service):
    mock_exchange_service.get_latest_rates.return_value = None

    use_case = GetLatestRatesUseCase(mock_exchange_service)

    result = await use_case.execute("EUR,BRL")

    assert result is None
    mock_exchange_service.get_latest_rates.assert_awaited_once_with(symbols="EUR,BRL")
