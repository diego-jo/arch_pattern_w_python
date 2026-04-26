from typing import Annotated, Any, Dict

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .db_config import get_session
from .model import OrderLine, allocate
from .repository import SqlAlchemyBatchRepository

app = FastAPI()


DBSession = Annotated[Session, Depends(get_session)]


@app.get("/health")
def health():
    return {"App": "ok", "DB": "ok"}


@app.post("/allocate-order")
def allocate_order(data: Dict[Any, Any], session: DBSession):
    repository = SqlAlchemyBatchRepository(session)
    order_line = OrderLine(
        orderid=data["orderId"], qty=int(data["qty"]), sku=data["sku"]
    )

    breakpoint()

    batches = repository.list()

    allocate(order_line, batches)

    session.commit()

    return 201
