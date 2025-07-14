from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment


@api_view(["POST"])
def check_payment_status(request, id):
    payment = get_object_or_404(Payment, id=id)

    return Response(
        {
            "id": payment.id,
            "amount": str(payment.amount),
            "currency": payment.currency,
            "payment_method": payment.payment_method,
            "reference": payment.reference,
            "status": payment.status,
        }
    )
