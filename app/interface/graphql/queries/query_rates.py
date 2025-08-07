import strawberry
import asyncio
from typing import Optional, List

from app.infrastructure.repositories.transaction_django import DjangoTransactionRepository
from app.interface.graphql.types.rates import RatesResponseType, Rate
from app.infrastructure.services.exchange_service import ExchangeService
from app.interface.graphql.types.types import TransactionType


@strawberry.type
class RatesQuery:
    @strawberry.field
    def latest_rates(self, symbols: Optional[str] = None) -> Optional[RatesResponseType]:
        service = ExchangeService()

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        result = loop.run_until_complete(
            service.get_latest_rates(symbols=symbols, format_response=True)
        )

        if result and result.get("rates"):
            rates_list = [Rate(currency=k, value=v) for k, v in result["rates"].items()]
            return RatesResponseType(
                base=result.get("base", ""),
                date=result.get("date", ""),
                rates=rates_list
            )
        return None

@strawberry.type
class TransactionQuery:
    @strawberry.field
    def all_transactions(self) -> List[TransactionType]:
        repository = DjangoTransactionRepository()
        transactions = repository.list()

        return [
            TransactionType(
                id=tx.id,
                amount=tx.amount,
                currency=tx.currency,
                category=tx.category,
                date=tx.date,
                description=tx.description
            ) for tx in transactions
        ]

    @strawberry.field
    def transaction_by_id(self, transaction_id: int) -> Optional[TransactionType]:
        repository = DjangoTransactionRepository()
        transactions = repository.list()
        transaction = next((t for t in transactions if t.id == transaction_id), None)

        if transaction:
            return TransactionType(
                id=transaction.id,
                amount=transaction.amount,
                currency=transaction.currency,
                category=transaction.category,
                date=transaction.date,
                description=transaction.description
            )
        return None
