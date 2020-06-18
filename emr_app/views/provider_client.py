import json 
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import ProviderClient, Provider, Client


class ProviderClientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProviderClient
        url = serializers.HyperlinkedIdentityField(
            view_name='providerclient',
            lookup_field='id'
        )
        fields = ('id', 'provider_id', 'client_id', 'client')
        depth = 2


class ProviderClients(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            provider = Provider.objects.get(pk=pk)
            serializer = ProviderSerializer(
                provider, context={
                    'request': request
                }
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        try:
            provider = Provider.objects.get(user=request.auth.user)
            providerclients = ProviderClient.objects.filter(provider=provider)
            serializer = ProviderClientSerializer(
                providerclients,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def create(self, request):
        req_body = json.loads(request.body.decode())
        
        provider = Provider.objects.get(pk=req_body['provider_id'])
        client = Client.objects.get(pk=req_body['client_id'])
        
        new_provider_client = ProviderClient()
        new_provider_client.provider = provider
        new_provider_client.client = client

        new_provider_client.save()

        serializer = ProviderClientSerializer(new_provider_client, context={'request': request})
        return Response(serializer.data)
