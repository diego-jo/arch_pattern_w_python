import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, Session

from orm import metadata, start_mappers


@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite:////home/diego/code/estudos/arch_pattern_w_python/ch2/test.db"
    )
    metadata.create_all(bind=engine)

    return engine


@pytest.fixture
def session(engine):
    start_mappers()
    with Session(engine) as session:
        yield session
    clear_mappers()
