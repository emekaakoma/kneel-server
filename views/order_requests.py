import sqlite3
from models import Order, Size, Style, Metal

ORDERS = [
    {
        "id": 1,
        "metal_id": 3,
        "size_id": 2,
        "style_id": 3,
        "timestamp": 1614659931693
    }
]


def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp,
            m.metal,
            m.price metal_price,
            si.carets,
            si.price size_price,
            s.style,
            s.price style_price
        FROM "Orders" o
        JOIN Metals m ON m.id = o.metal_id
        JOIN Sizes si ON si.id = o.size_id
        JOIN Styles s ON s.id = o.style_id
        """)

        orders = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            order = Order(row['id'], row['metal_id'], row['size_id'],
                            row['style_id'], row['timestamp'])
            
            metal = Metal(row['id'], row['metal'], row['metal_price'])
            size = Size(row['id'], row['carets'], row['size_price'])
            style = Style(row['id'], row['style'], row['style_price'])

            order.metal = metal.__dict__
            order.size = size.__dict__
            order.style = style.__dict__

            orders.append(order.__dict__)

    return orders


def get_single_order(id):
   with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp
        FROM "Orders" o
        WHERE o.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        order = Order(data['id'], data['metal_id'], data['size_id'], data['style_id'], data['timestamp'])

        return order.__dict__


def create_order(order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO "Orders"
            ( metal_id, size_id, style_id, timestamp)
        VALUES
            ( ?, ?, ?, ?);
        """, (order['metal_id'], order['size_id'],
              order['style_id'], order['timestamp'], ))

        id = db_cursor.lastrowid
        order['id'] = id


    return order


def delete_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM "Orders"
        WHERE id = ?
        """, (id, ))


def update_order(id, new_order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE "Orders"
            SET
                metal_id = ?,
                size_id = ?,
                style_id = ?,
                timestamp = ?
        WHERE id = ?
        """, (new_order['metal_id'], new_order['size_id'],
              new_order['style_id'], new_order['timestamp'], id, ))
        
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
