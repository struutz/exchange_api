from abc import ABC

from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.db.models.transaction_model import TransactionModel


class DjangoTransactionRepository(TransactionRepository, ABC):
    def list(self):
        return [self._to_entity(obj) for obj in TransactionModel.objects.all()]

    def create(self, transaction: Transaction):
        obj = TransactionModel.objects.create(**transaction.__dict__)

        return self._to_entity(obj)

    def update(self, transaction: Transaction):
        obj = TransactionModel.objects.get(pk=transaction.id)

        for field, value in transaction.__dict__.items():
            setattr(obj, field, value)

        obj.save()

        return self._to_entity(obj)

    def delete(self, transaction_id: int):
        TransactionModel.objects.get(pk=transaction_id).delete()

        return True

    @staticmethod
    def _to_entity(obj):
        return Transaction(
            id=obj.id,
            amount=obj.amount,
            currency=obj.currency,
            category=obj.category,
            date=obj.date,
            description=obj.description
        )