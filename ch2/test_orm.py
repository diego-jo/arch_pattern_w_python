from sqlalchemy import text, select
import model


def test_orderline_mappers_can_load_lines(session):
    session.execute(
        text(
            "INSERT INTO order_lines (orderid, sku, qty) VALUES "
            "('order1', 'RED-CHAIR', 12),"
            "('order1', 'RED-CHAIR', 13),"
            "('order2', 'RED-TABLE', 10)"
        )
    )

    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-CHAIR", 13),
        model.OrderLine("order2", "RED-TABLE", 10),
    ]

    assert session.scalars(select(model.OrderLine)).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order23", "RED-TABLE", 10)

    session.add(new_line)
    session.commit()

    result = session.scalar(select(model.OrderLine))

    assert result == new_line
