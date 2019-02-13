# -*- coding: utf-8 -*-
#

from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from common.permissions import IsOrgAdminOrAppUser
from common.utils import get_object_or_none
from ..models import Asset
from ..backends.credentials import credential_backend
from ..serializers import CredentialSerializer, CredentialAuthInfoSerializer


class CredentialViewSet(viewsets.GenericViewSet):
    serializer_class = CredentialSerializer
    http_method_names = ['get', 'post']
    permission_classes = (IsOrgAdminOrAppUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        username = self.request.GET.get('username', None)
        latest = self.request.GET.get('latest') == '1'
        asset_id = self.request.GET.get('asset_id', None)
        asset = get_object_or_none(Asset, pk=asset_id)

        queryset = credential_backend.filter(
            asset=asset, username=username, latest=latest
        )
        return queryset


class CredentialAuthInfoApi(generics.RetrieveAPIView):
    serializer_class = CredentialAuthInfoSerializer
    permission_classes = (IsOrgAdminOrAppUser,)

    def get_object(self):
        pk = self.kwargs.get('pk')
        instance = credential_backend.get(pk=pk)
        return instance