import csv

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.db import connection


def is_admin(user):
    return user.is_authenticated and (
        user.is_superuser or user.role == "admin"
    )


@user_passes_test(is_admin)
def export_orders_csv(request):
    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = (
        'attachment; filename="orders_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Order ID",
        "User ID",
        "Total",
        "Payment Status",
        "Order Status",
        "Order Date",
        "Product ID",
        "Product Name",
        "Quantity",
        "Product Price",
    ])

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                o.id,
                o.user_id,
                o.total,
                o.payment_status,
                o.order_status,
                o.timestamp,
                oi.product_id,
                p.name,
                oi.quantity,
                oi.price
            FROM orders o
            LEFT JOIN order_items oi
                ON oi.order_id = o.id
            LEFT JOIN products p
                ON p.id = oi.product_id
            ORDER BY o.timestamp DESC, o.id DESC
        """)

        rows = cursor.fetchall()

    for row in rows:
        writer.writerow(row)

    return response


@user_passes_test(is_admin)
def export_orders_pdf(request):
    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        'attachment; filename="orders_report.pdf"'
    )

    document = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Smart E-Commerce - Orders Report",
        styles["Title"],
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    data = [[
        "Order ID",
        "User ID",
        "Total",
        "Payment",
        "Order Status",
        "Product",
        "Qty",
        "Price",
    ]]

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                o.id,
                o.user_id,
                o.total,
                o.payment_status,
                o.order_status,
                p.name,
                oi.quantity,
                oi.price
            FROM orders o
            LEFT JOIN order_items oi
                ON oi.order_id = o.id
            LEFT JOIN products p
                ON p.id = oi.product_id
            ORDER BY o.timestamp DESC, o.id DESC
        """)

        rows = cursor.fetchall()

    for row in rows:
        data.append([
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5] or "",
            row[6] or "",
            row[7] or "",
        ])

    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.grey,
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white,
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.black,
        ),
        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold",
        ),
        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            8,
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE",
        ),
    ]))

    elements.append(table)

    document.build(elements)

    return response