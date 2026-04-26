from datetime import date, timedelta

import pytest
from .model import Batch, OrderLine, OutOfStock, allocate

BIG_CHAIR_SKU = "BIG_CHAIR_001"
BIG_TABLE_SKU = "BIG_TABLE_001"


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku=sku, qty=batch_qty, eta=date.today()),
        OrderLine("order-001", sku=sku, qty=line_qty),
    )


def test_allocating_to_a_batch_reduces_available_quantity():
    batch = Batch("batch-01", BIG_CHAIR_SKU, qty=10, eta=None)
    line = OrderLine("order-ref", BIG_CHAIR_SKU, 2)

    batch.allocate(line)

    assert batch.available_quantity == 8


def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_line(BIG_CHAIR_SKU, 10, 5)

    assert batch.can_allocate(line)


def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = make_batch_and_line(BIG_CHAIR_SKU, 2, 5)

    assert batch.can_allocate(line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line(BIG_CHAIR_SKU, 5, 5)

    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-01", BIG_CHAIR_SKU, qty=10, eta=None)
    line = OrderLine("order-ref", BIG_TABLE_SKU, 2)

    assert batch.can_allocate(line) is False


def test_can_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line(BIG_TABLE_SKU, 20, 15)
    batch.deallocate(unallocated_line)

    assert batch.available_quantity == 20


def test_allocation_is_idempotent():
    batch, line = make_batch_and_line(BIG_CHAIR_SKU, 10, 5)

    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == 5


def test_prefers_current_stock_batch_to_shipments():
    today = date.today()
    in_stock_batch = Batch("in_stock_batch", BIG_CHAIR_SKU, qty=10, eta=None)
    shipment_batch = Batch("shipment_batch", BIG_CHAIR_SKU, qty=10, eta=today)
    line = OrderLine("order_ref", BIG_CHAIR_SKU, 5)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 5
    assert shipment_batch.available_quantity == 10


def test_prefers_earlier_batches():
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    later = date.today() + timedelta(days=10)

    today_batch = Batch("in_stock_batch", BIG_CHAIR_SKU, qty=10, eta=today)
    tomorrow_batch = Batch("shipment_batch", BIG_CHAIR_SKU, qty=10, eta=tomorrow)
    latest_batch = Batch("shipment_batch", BIG_CHAIR_SKU, qty=10, eta=later)
    line = OrderLine("order_ref", BIG_CHAIR_SKU, 5)

    allocate(line, [today_batch, tomorrow_batch, latest_batch])

    assert today_batch.available_quantity == 5
    assert tomorrow_batch.available_quantity == 10
    assert latest_batch.available_quantity == 10


def test_return_allocated_batch_reference():
    today = date.today()
    in_stock_batch = Batch("in_stock_batch", BIG_CHAIR_SKU, qty=10, eta=None)
    shipment_batch = Batch("shipment_batch", BIG_CHAIR_SKU, qty=10, eta=today)
    line = OrderLine("order_ref", BIG_CHAIR_SKU, 5)

    allecated_ref = allocate(line, [in_stock_batch, shipment_batch])

    assert allecated_ref == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch-ref", BIG_TABLE_SKU, 100, eta=date.today)
    allocate(OrderLine("order1", BIG_TABLE_SKU, 100), [batch])

    with pytest.raises(OutOfStock, match=BIG_TABLE_SKU):
        allocate(OrderLine("order2", BIG_TABLE_SKU, 1), [batch])
