from .db_config import get_session
from .repository import SqlAlchemyBatchRepository


def get_batch_repository() -> SqlAlchemyBatchRepository:
    return SqlAlchemyBatchRepository(get_session())
