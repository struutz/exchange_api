from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import TransactionRepository


class CreateTransactionUseCase:
    def __init__(self, transaction_repository: TransactionRepository):
        self.repository = transaction_repository

    def execute(self, transaction: Transaction):
        return self.repository.create(transaction)
