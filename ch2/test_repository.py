from sqlalchemy import text

from .model import Batch, OrderLine
from .repository import SqlAlchemyBatchRepository


def insert_order_line(session):
    session.execute(
        text(
            "INSERT INTO order_lines (orderid, sku, qty)"
            ' VALUES ("order1", "BLUE_TABLE", 15)'
        )
    )
    [[orderline_id]] = session.execute(
        text("SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku"),
        dict(orderid="order1", sku="BLUE_TABLE"),
    )
    return orderline_id


def insert_batch(session, batch_id):
    session.execute(
        text(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
            ' VALUES (:batch_id, "BLUE_TABLE", 100, null)'
        ),
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        text('SELECT id FROM batches WHERE reference=:batch_id AND sku="BLUE_TABLE"'),
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        text(
            "INSERT INTO allocations (orderline_id, batch_id)"
            " VALUES (:orderline_id, :batch_id)"
        ),
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


def test_repository_can_save_a_batch(session):
    batch = Batch("batch1", "RED_TABLE", 100, eta=None)

    repo = SqlAlchemyBatchRepository(session)
    repo.add(batch)
    session.commit()

    rows = list(
        session.execute(
            text("SELECT reference, sku, _purchased_quantity, eta FROM 'batches'")
        )
    )

    assert rows == [("batch1", "RED_TABLE", 100, None)]


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch_id1 = insert_batch(session, "batch2")
    insert_batch(session, "batch3")
    insert_allocation(session, orderline_id, batch_id1)

    repo = SqlAlchemyBatchRepository(session)
    retrieved = repo.get("batch2")

    expected = Batch("batch2", "BLUE_TABLE", 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {OrderLine("order1", "BLUE_TABLE", 15)}
