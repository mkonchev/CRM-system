from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def api_overview(request):
    api_urls = {
        "all_items": "/model_name/",
        "Add": "/model_name/create",
        "GET": "/model_name/<int:pk>",
        "Update": "/model_name/<int:pk>",
        "Delete": "/model_name/<int:pk>",
    }
    return Response(api_urls, status=status.HTTP_200_OK)
