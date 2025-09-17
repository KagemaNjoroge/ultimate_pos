from datetime import datetime, timedelta
from sales.models import SaleItem
from sales.models import Sale
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sales.serializers import SaleSerializer


@api_view(["GET"])
def duration_sales_report(request):
    # get duration span
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)

    if start_date and end_date:
        sales = Sale.objects.filter(created_at__range=[start_date, end_date])
    else:
        # return for the past month
        sales = Sale.objects.filter(
            created_at__range=[
                datetime.now().replace(day=1),
                datetime.now().replace(day=31),
            ]
        )
    serializer = SaleSerializer(sales, many=True)

    return Response(
        data=serializer.data,
        status=200,
    )


@api_view(["GET"])
def sales_this_month(request) -> Response:

    sales = Sale.objects.filter(
        created_at__range=[
            datetime.now() - timedelta(days=28),
            datetime.now(),
        ]
    )

    total = sum([sale.grand_total for sale in sales])
    serializer = SaleSerializer(sales, many=True)

    return Response(
        data={
            "total": total,
            "sales": serializer.data,
            "count": sales.count(),
        },
        status=200,
    )


@api_view(["GET"])
def sales_this_week(request) -> Response:
    sales = Sale.objects.filter(
        created_at__range=[datetime.now() - timedelta(days=7), datetime.now()]
    )

    serializer = SaleSerializer(sales, many=True)

    total = sum([sale.grand_total for sale in sales])

    return Response(
        data={
            "total": total,
            "sales": serializer.data,
            "count": sales.count(),
        },
        status=200,
    )


@api_view(["GET"])
def best_selling_product(request) -> Response:
    sales = Sale.objects.filter(
        created_at__range=[
            datetime.now() - timedelta(days=28),
            datetime.now(),
        ]
    )
    if not sales:
        return Response(
            data={"top_selling": "No sales made"},
            status=200,
        )

    tops = {}
    sale_items = SaleItem.objects.filter(sale__in=sales)
    # count sale_item.product
    if not sale_items:
        # 404
        return Response(
            data={"top_selling": "No sales made"},
            status=404,
        )
    for item in sale_items:
        if item.product.name in tops:
            tops[item.product.name] += item.quantity
        else:
            tops[item.product.name] = item.quantity

    tops = sorted(tops.items(), key=lambda x: x[1], reverse=True)[0]

    return Response(
        data={"top_selling": tops},
        status=200,
    )


@api_view(["GET"])
def get_best_selling_category(request) -> Response:

    sales = Sale.objects.filter(
        created_at__range=[
            datetime.now().replace(day=1),
            datetime.now().replace(day=30),
        ]
    )

    sale_items = SaleItem.objects.filter(sale__in=sales)
    if not sale_items:
        # 404
        return Response(
            data={"top_selling": "No sales made"},
            status=404,
        )

    else:
        tops = {}
        for item in sale_items:
            if item.product.category.name in tops:
                tops[item.product.category.name] += item.quantity
            else:
                tops[item.product.category.name] = item.quantity

        tops = sorted(tops.items(), key=lambda x: x[1], reverse=True)[0]

        return Response(
            data={
                "category": tops[0],
                "quantity": tops[1],
                "sales": SaleSerializer(sales, many=True).data,
                "count": sales.count(),
                "total_sales": sum(sale.grand_total for sale in sales),
                "total_transactions": sales.count(),
            },
            status=200,
        )
