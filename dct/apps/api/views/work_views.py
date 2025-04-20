from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.api.serializers.WorkSerializer import WorkSerializer
from apps.work.models.WorkModel import Work


@api_view(['GET'])
def work_list_view(request):
    work_list = Work.objects.all()
    serializer = WorkSerializer(work_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def work_by_id(request, pk):
    work = Work.objects.get(pk=pk)
    serializer = Work(work)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
