import uuid
from hashlib import sha512

from django.contrib.auth import authenticate, login
from django.http import HttpRequest

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework.pagination import PageNumberPagination

from server.views.serializer import (
    DatasetRecordSerialzier,
    DatasetUpdateSerializer,
    DatasetCreateSerializer

)
from server.models import (
    InstructionTree,
    UserInstructionTree,
    APIKEY,
    FineGrainAPIKEY,
    MemoryTree,
    Dataset,
    DatasetRecord
)
from server.utils.sync_.manage_permissions import get_master_key_and_master_user
from server.utils import constant


@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
@permission_classes([IsAuthenticated])
def get_default_user_dataset_api(request):
    current_user = request.user
    if not current_user.has_perm('server.allow_create_dataset'):
        return Response({'detail': "Not authorised to create dataset"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        dataset_serializer = DatasetCreateSerializer()

        master_key, master_user = get_master_key_and_master_user(
            current_user=current_user)
        if Dataset.objects.filter(user=master_user).count() == 0:
            return Response({'detail': "No Dataset"}, status=status.HTTP_200_OK)
        else:
            dataset_list = Dataset.objects.filter(user=master_user)
            default_dataset = dataset_list.latest("id")
            paginator = PageNumberPagination()
            paginator.page_size = 10
            records = DatasetRecord.objects.filter(dataset=default_dataset)
            result_records = paginator.paginate_queryset(records, request)
            record_serializer = DatasetRecordSerialzier(
                result_records, many=True)
            dataset_serializer = DatasetCreateSerializer(default_dataset)
            dataset_list_serializer = DatasetCreateSerializer(
                default_dataset, many=True)
            return paginator.get_paginated_response({
                dataset_list: dataset_list_serializer.data,
                default_dataset: dataset_serializer.data,
                record_serializer: record_serializer.data
            })


@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
@permission_classes([IsAuthenticated])
def create_user_dataset_api(request):
    current_user = request.user
    if not current_user.has_perm('server.allow_create_dataset'):
        return Response({'detail': "Not authorised to create dataset"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = DatasetCreateSerializer(
            data=request.data)
        if serializer.is_valid():
            dataset_name = serializer.data['name']
            master_key, master_user = get_master_key_and_master_user(
                current_user=current_user)
            if Dataset.objects.filter(user=master_user).count() <= constant.MAX_DATASET_PER_USER:
                Dataset.objects.create(user=master_user, name=dataset_name)
                return Response({'detail': "Saved"}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "Save Failed!, you have react maximun number of datasets"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': "Save Failed!, ensure that fields do not contain empty string"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@throttle_classes([AnonRateThrottle])
@permission_classes([IsAuthenticated])
def update_user_dataset_api(request):
    current_user = request.user
    if not current_user.has_perm('server.allow_create_dataset'):
        return Response({'detail': "Not authorised to create dataset"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = DatasetUpdateSerializer(
            data=request.data)
        if serializer.is_valid():
            dataset_name = serializer.data['name']
            new_dataset_name = serializer.data['new_name']
            master_key, master_user = get_master_key_and_master_user(
                current_user=current_user)
            try:
                dataset = Dataset.objects.get(
                    user=master_user, name=dataset_name)
                dataset.name = new_dataset_name
                dataset.save()
                return Response({'detail': "Saved"}, status=status.HTTP_200_OK)
            except Dataset.DoesNotExist:
                return Response({'detail': "Failed, Cannot fine your dataset"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': "Save Failed!, ensure that fields do not contain empty string"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@throttle_classes([AnonRateThrottle])
@permission_classes([IsAuthenticated])
def delete_user_dataset_api(request):
    current_user = request.user
    if not current_user.has_perm('server.allow_create_dataset'):
        return Response({'detail': "Not authorised to create dataset"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = DatasetCreateSerializer(
            data=request.data)
        if serializer.is_valid():
            dataset_name = serializer.data['name']
            master_key, master_user = get_master_key_and_master_user(
                current_user=current_user)
            try:
                dataset = Dataset.objects.get(
                    name=dataset_name, user=master_user)
                dataset.delete()
                return Response({'detail': "Deleted"}, status=status.HTTP_200_OK)
            except Dataset.DoesNotExist:
                return Response({'detail': "Dataset does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': "Save Failed!, ensure that fields do not contain empty string!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
@permission_classes([IsAuthenticated])
def create_user_record_api(request):
    current_user = request.user
    if not current_user.has_perm('server.allow_create_dataset'):
        return Response({'detail': "Not authorised to create dataset"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = DatasetRecordSerialzier(
            data=request.data)
        if serializer.is_valid():
            dataset_name = serializer.data['dataset']
            system_prompt = serializer.data['system_prompt']
            prompt = serializer.data['prompt']
            response = serializer.data['response']
            evaluation = serializer.data['evaluation']
            master_key, master_user = get_master_key_and_master_user(
                current_user=current_user)
            try:
                dataset = Dataset.objects.get(
                    user=master_key, name=dataset_name)
                DatasetRecord.objects.create(
                    user=master_user, dataset=dataset, system_prompt=system_prompt, prompt=prompt, response=response, evaluation=evaluation)
                return Response({'detail': "Saved"}, status=status.HTTP_200_OK)
            except Dataset.DoesNotExist:
                return Response({'detail': "Dataset does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': "Save Failed!, ensure that fields do not contain empty string"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@throttle_classes([AnonRateThrottle])
@permission_classes([IsAuthenticated])
def update_user_record_api(request):
    current_user = request.user
    if not current_user.has_perm('server.allow_create_dataset'):
        return Response({'detail': "Not authorised to create dataset"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = DatasetRecordSerialzier(
            data=request.data)
        if serializer.is_valid():
            dataset_name = serializer.data['dataset']
            system_prompt = serializer.data['system_prompt']
            prompt = serializer.data['prompt']
            response = serializer.data['response']
            evaluation = serializer.data['evaluation']
            id = serializer.data['id']
            master_key, master_user = get_master_key_and_master_user(
                current_user=current_user)
            try:
                dataset = Dataset.objects.get(
                    user=master_key, name=dataset_name)
            except Dataset.DoesNotExist:
                return Response({'detail': "Dataset does not exist"}, status=status.HTTP_404_NOT_FOUND)
            try:
                record = DatasetRecord.objects.get(
                    user=master_user, dataset=dataset, id=id)
                record.system_prompt = system_prompt
                record.prompt = prompt
                record.response = response
                record.evaluation = evaluation
                record.save()
                return Response({'detail': "Saved"}, status=status.HTTP_200_OK)
            except DatasetRecord.DoesNotExist:
                return Response({'detail': "Record does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': "Save Failed!, ensure that fields do not contain empty string"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@throttle_classes([AnonRateThrottle])
@permission_classes([IsAuthenticated])
def delete_user_record_api(request):
    current_user = request.user
    if not current_user.has_perm('server.allow_create_dataset'):
        return Response({'detail': "Not authorised to create dataset"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        serializer = DatasetRecordSerialzier(
            data=request.data)
        if serializer.is_valid():
            id = serializer.data['id']
            dataset_name = serializer.data['dataset']

            master_key, master_user = get_master_key_and_master_user(
                current_user=current_user)
            try:
                dataset = Dataset.objects.get(
                    user=master_key, name=dataset_name)
            except Dataset.DoesNotExist:
                return Response({'detail': "Dataset does not exist"}, status=status.HTTP_404_NOT_FOUND)
            try:
                record = DatasetRecord.objects.get(
                    user=master_user, dataset=dataset, id=id)
                record.delete()
                return Response({'detail': "Saved"}, status=status.HTTP_200_OK)
            except DatasetRecord.DoesNotExist:
                return Response({'detail': "Record does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': "Save Failed!, ensure that fields do not contain empty string"}, status=status.HTTP_404_NOT_FOUND)