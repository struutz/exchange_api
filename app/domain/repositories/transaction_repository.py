from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.transaction import Transaction


class TransactionRepository(ABC):
    @abstractmethod
    def list(self) -> List[Transaction]:
        pass

    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    def update(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    def delete(self, transaction_id: int) -> bool:
        pass
    