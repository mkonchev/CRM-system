from rest_framework import status, serializers
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


@api_view(['POST'])
def add_workstatus(request):
    workstatus = WorkstatusSerializer(data=request.data)

    # if user.objects.filter(**request.data).exists():
    #     raise serializers.ValidationError('This data already exists')

    if workstatus.is_valid():
        workstatus.save()
        return Response(data=workstatus.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_workstatus(request, pk):
    workstatus = Workstatus.objects.get(pk=pk)
    workstatus = WorkstatusSerializer(instance=workstatus, data=request.data)

    if workstatus.is_valid():
        workstatus.save()
        return Response(data=workstatus.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_workstatus(request, pk):
    if Workstatus.objects.filter(pk=pk).exists():
        workstatus = Workstatus.objects.get(pk=pk)
        workstatus.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        raise serializers.ValidationError('Not found this data')
