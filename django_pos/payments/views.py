from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ResponseData
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="post",
    operation_summary="Handle M-Pesa Daraja Callback",
    responses={201: "Response data saved successfully.", 500: "Internal Server Error"},
    tags=["Payments"],
)
@api_view(["POST"])
def mpesa_daraja_callback(request):
    """
    Endpoint to handle the callback from the M-Pesa Daraja API.
    This endpoint will receive the response data and save it to the database.
    """
    try:
        response_data = request.data
        # Save the response data to the database
        ResponseData.objects.create(response_data=response_data)
        return Response(
            {"status": "success", "message": "Response data saved successfully."},
            status=201,
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error("An error occurred while processing the M-Pesa Daraja callback.", exc_info=True)
        return Response({"status": "error", "message": "An internal error occurred. Please try again later."}, status=500)
