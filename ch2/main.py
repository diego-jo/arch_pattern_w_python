from typing import Any, Dict

from fastapi import FastAPI, Depends
from sqlalchemy import select

from .db_config import get_session
from .model import Batch, OrderLine, allocate

app = FastAPI()


@app.get("/health")
def health():
    return {"App": "ok", "DB": "ok"}


@app.post("/allocate-order")
def allocate_order(data: Dict[Any, Any], session=Depends(get_session)):
    order_line = OrderLine(
        orderid=data["orderId"], qty=int(data["qty"]), sku=data["sku"]
    )

    batches = session.scalars(select(Batch)).all()

    allocate(order_line, batches)

    session.commit()

    return 201
