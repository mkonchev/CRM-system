from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'all_items': '/model_name/',
        'search_by_id': '/model_name/<int:pk>',
        'Add': '/model_name/create',
        'Update': '/model_name/update',
        'Delete': '/model_name/delete'
    }
    return Response(api_urls, status=status.HTTP_200_OK)
