import datetime

import pytest
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.domain.entities.transaction import Transaction
from app.infrastructure.repositories.transaction_django import DjangoTransactionRepository


@pytest.fixture
def repo():
    return DjangoTransactionRepository()


@pytest.fixture
def transaction():
    return Transaction(
        id=1,
        amount=Decimal("120.50"),
        currency="EUR",
        category="Food",
        date=datetime.datetime.now(),
        description="Lunch"
    )

def test_list_transactions(repo, mocker):
    mock_obj = mocker.MagicMock()
    mock_obj.id = 1
    mock_obj.amount = Decimal("100.00")
    mock_obj.currency = "EUR"
    mock_obj.category = "Food"
    mock_obj.date = date(2023, 1, 1)
    mock_obj.description = "Lunch"

    mocker.patch(
        "app.infrastructure.repositories.transaction_django.TransactionModel.objects.all",
        return_value=[mock_obj]
    )

    result = repo.list()

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].currency == "EUR"


def test_create_transaction(repo, transaction, mocker):
    mock_obj = mocker.MagicMock()
    mock_obj.id = 1
    mock_obj.amount = transaction.amount
    mock_obj.currency = transaction.currency
    mock_obj.category = transaction.category
    mock_obj.date = transaction.date
    mock_obj.description = transaction.description

    mock_create = mocker.patch(
        "app.infrastructure.repositories.transaction_django.TransactionModel.objects.create",
        return_value=mock_obj
    )

    result = repo.create(transaction)

    mock_create.assert_called_once()
    assert result.id == 1
    assert result.currency == "EUR"


def test_update_transaction(repo, transaction, mocker):
    mock_obj = mocker.MagicMock()
    mock_get = mocker.patch(
        "app.infrastructure.repositories.transaction_django.TransactionModel.objects.get",
        return_value=mock_obj
    )

    result = repo.update(transaction)

    mock_get.assert_called_once_with(pk=transaction.id)
    assert result.currency == "EUR"
    mock_obj.save.assert_called_once()


def test_delete_transaction(repo, transaction, mocker):
    mock_obj = mocker.MagicMock()
    mock_get = mocker.patch(
        "app.infrastructure.repositories.transaction_django.TransactionModel.objects.get",
        return_value=mock_obj
    )

    repo.delete(transaction.id)

    mock_get.assert_called_once_with(pk=transaction.id)
    mock_obj.delete.assert_called_once()