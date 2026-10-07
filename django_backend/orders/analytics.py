from django.db import connection


def get_total_sales():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COALESCE(SUM(total), 0)
            FROM orders
            WHERE payment_status = 'paid'
        """)
        return float(cursor.fetchone()[0])


def get_total_orders():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*)
            FROM orders
        """)
        return cursor.fetchone()[0]


def get_top_selling_products():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                oi.product_id,
                SUM(oi.quantity) AS total_quantity
            FROM order_items oi
            INNER JOIN orders o ON o.id = oi.order_id
            WHERE o.payment_status = 'paid'
            GROUP BY oi.product_id
            ORDER BY total_quantity DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()

    return [
        {
            "product_id": row[0],
            "quantity_sold": row[1],
        }
        for row in rows
    ]


def get_revenue_trends():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                DATE(timestamp) AS order_date,
                COALESCE(SUM(total), 0) AS revenue
            FROM orders
            WHERE payment_status = 'paid'
            GROUP BY DATE(timestamp)
            ORDER BY order_date ASC
        """)

        rows = cursor.fetchall()

    return [
        {
            "date": str(row[0]),
            "revenue": float(row[1]),
        }
        for row in rows
    ]


def get_low_stock_products():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                id,
                name,
                stock
            FROM products
            WHERE stock <= 5
            ORDER BY stock ASC
        """)

        rows = cursor.fetchall()

    return [
        {
            "product_id": row[0],
            "name": row[1],
            "stock": row[2],
        }
        for row in rows
    ]