from django.urls import path

from .views import analytics_dashboard
from .reports import export_orders_csv, export_orders_pdf

urlpatterns = [
    path("analytics/", analytics_dashboard, name="analytics"),

    path("reports/orders/csv/", export_orders_csv, name="orders_csv", ),

    path("reports/orders/pdf/", export_orders_pdf,name="orders_pdf",),
]