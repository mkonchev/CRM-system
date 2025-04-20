from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.api.serializers.WorkstatusSerializer import WorkstatusSerializer
from apps.workstatus.models.WorkstatusModel import Workstatus


@api_view(['GET'])
def workstatus_list_view(request):
    workstatus_list = Workstatus.objects.all()
    serializer = WorkstatusSerializer(workstatus_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def workstatus_by_id(request, pk):
    workstatus = Workstatus.objects.get(pk=pk)
    serializer = Workstatus(workstatus)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
