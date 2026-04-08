from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from .orm import metadata, start_mappers

engine = create_engine(
    "sqlite:////home/diego/code/estudos/arch_pattern_w_python/ch2/dev.db"
)

metadata.create_all(bind=engine)
start_mappers()


def get_session():
    return Session(bind=engine)
