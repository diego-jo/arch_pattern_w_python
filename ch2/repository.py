from typing import List
from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: str) -> Batch:
        raise NotImplementedError


class SqlAlchemyBatchRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, batch: Batch):
        self.session.add(batch)

    def get(self, reference: str) -> Batch:
        return self.session.scalar(select(Batch).where(Batch.reference == reference))

    def list(self) -> List[Batch]:
        return self.session.scalars(select(Batch)).all()


class FakeBatchRepository(AbstractRepository):
    def __init__(self, batches: List[Batch]):
        self._batches = set(batches)

    def add(self, batch: Batch):
        self._batches.add(batch)

    def get(self, ref: str) -> Batch:
        return next(batch for batch in self._batches if batch.reference == ref)

    def list(self) -> List[Batch]:
        return list(self._batches)
