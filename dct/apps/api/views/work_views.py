from rest_framework import status, serializers
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
def work_by_id_view(request, pk):
    try:
        work = Work.objects.get(pk=pk)
        serializer = WorkSerializer(work)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Work.DoesNotExist:
        return Response(
            {"detail": "Работа не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def add_work_view(request):
    work = WorkSerializer(data=request.data)

    # if user.objects.filter(**request.data).exists():
    #     raise serializers.ValidationError('This data already exists')

    if work.is_valid():
        work.save()
        return Response(data=work.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_work_view(request, pk):
    try:
        work = Work.objects.get(pk=pk)
        upd_work = WorkSerializer(instance=work, data=request.data, partial=True)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if upd_work.is_valid():
        upd_work.save()
        return Response(data=upd_work.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_work_view(request, pk):
    if Work.objects.filter(pk=pk).exists():
        work = Work.objects.get(pk=pk)
        work.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        raise serializers.ValidationError('Not found this data')
