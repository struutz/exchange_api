from datetime import datetime
from decimal import Decimal

import pytest
from unittest.mock import Mock

from app.application.use_cases.create_transaction import CreateTransactionUseCase
from app.domain.entities.transaction import Transaction


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def transaction():
    return Transaction(
        id=1,
        amount=Decimal(100),
        category="Test",
        currency="EUR",
        date=datetime.now(),
        description=""
    )


def test_execute_calls_repository_create(mock_repository, transaction):
    # Arrange
    mock_repository.create.return_value = transaction
    use_case = CreateTransactionUseCase(mock_repository)

    # Act
    result = use_case.execute(transaction)

    # Assert
    mock_repository.create.assert_called_once_with(transaction)
    assert result == transaction
