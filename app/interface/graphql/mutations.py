import asyncio
from decimal import Decimal
from typing import Optional
import strawberry
from datetime import datetime

from app.domain.entities.transaction import Transaction
from app.infrastructure.services.exchange_service import ExchangeService
from app.infrastructure.repositories.transaction_django import DjangoTransactionRepository
from app.interface.graphql.types.types import TransactionType, ConversionResultType


@strawberry.type
class TransactionMutation:
    @strawberry.mutation
    def create_transaction(
        self,
        amount: Decimal,
        currency: str,
        category: str,
        date: datetime,
        description: str
    ) -> TransactionType:
        repository = DjangoTransactionRepository()
        transaction = Transaction(
            amount=amount,
            currency=currency,
            category=category,
            date=date,
            description=description
        )
        created = repository.create(transaction)

        return TransactionType(
            id=created.id,
            amount=created.amount,
            currency=created.currency,
            category=created.category,
            date=created.date,
            description=created.description
        )

    @strawberry.mutation
    def update_transaction(
        self,
        transaction_id: int,
        amount: Decimal,
        currency: str,
        category: str,
        date: datetime,
        description: str
    ) -> Optional[TransactionType]:
        repository = DjangoTransactionRepository()
        updated = repository.update(Transaction(
            id=transaction_id,
            amount=amount,
            currency=currency,
            category=category,
            date=date,
            description=description))
        return TransactionType(
            id=updated.id,
            amount=updated.amount,
            currency=updated.currency,
            category=updated.category,
            date=updated.date,
            description=updated.description
        )

    @strawberry.mutation
    def delete_transaction(self, transaction_id: int) -> bool:
        repository = DjangoTransactionRepository()
        return repository.delete(transaction_id)

    @strawberry.mutation
    def convert_currency(
        self,
        from_currency: str,
        to_currency_target: str,
        amount: Decimal
    ) -> Optional[ConversionResultType]:
        service = ExchangeService()

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            service.convert(from_currency, to_currency_target, amount)
        )
