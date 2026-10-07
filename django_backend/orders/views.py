from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

from .analytics import (
    get_total_sales,
    get_total_orders,
    get_top_selling_products,
    get_revenue_trends,
    get_low_stock_products,
)


def is_admin(user):
    return user.is_authenticated and (
        user.is_superuser or user.role == "admin"
    )


@user_passes_test(is_admin)
def analytics_dashboard(request):
    return JsonResponse({
        "total_sales": get_total_sales(),
        "total_orders": get_total_orders(),
        "top_selling_products": get_top_selling_products(),
        "revenue_trends": get_revenue_trends(),
        "low_stock_products": get_low_stock_products(),
    })