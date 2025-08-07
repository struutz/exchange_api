import pytest
from decimal import Decimal
from unittest.mock import AsyncMock

from app.application.use_cases.convert_currency_use_case import ConvertCurrencyUseCase
from app.domain.services.exchange_service import ExchangeService


@pytest.mark.asyncio
async def test_convert_currency_success():
    # Arrange
    mock_service = AsyncMock(spec=ExchangeService)
    mock_service.convert.return_value = Decimal('50.0')

    use_case = ConvertCurrencyUseCase(exchange_service=mock_service)

    # Act
    result = await use_case.execute(
        from_currency="USD",
        to_currency="EUR",
        amount=Decimal('100.0'),
        to_currency_target="BRL"
    )

    # Assert
    assert result == Decimal('50.0')
    mock_service.convert.assert_awaited_once_with("USD", "EUR", Decimal('100.0'), "BRL")


@pytest.mark.asyncio
async def test_convert_currency_service_raises_exception():
    # Arrange
    mock_service = AsyncMock(spec=ExchangeService)
    mock_service.convert.side_effect = Exception("Conversion failed")

    use_case = ConvertCurrencyUseCase(exchange_service=mock_service)

    # Act & Assert
    with pytest.raises(Exception, match="Conversion failed"):
        await use_case.execute(
            from_currency="USD",
            to_currency="EUR",
            amount=Decimal('100.0'),
            to_currency_target="BRL"
        )
