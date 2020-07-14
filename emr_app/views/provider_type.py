"""View module for handling requests about Providers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import ProviderType


class ProviderTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProviderType
        url = serializers.HyperlinkedIdentityField(
            view_name='providertype',
            lookup_field='id'
        )
        fields = ('id', 'name')

class ProviderTypes(ViewSet):
    def retrieve(self, request, pk=None):
        provider_type = ProviderType.objects.get(pk=pk)
        serializer = ProviderTypeSerializer(provider_type, context={'request': request})
        return Response(serializer.data)
    
    def list(self, request):
        provider_types = ProviderType.objects.all()
        serializer = ProviderTypeSerializer(provider_types, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        provider_type = ProviderType()
        
        provider_type.name = request.data["name"]

        provider_type.save()

        serializer = ProviderTypeSerializer(provider_type, context={'request': request})
        return Response(serializer.data)