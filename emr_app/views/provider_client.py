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
        fields = ('id', 'provider_id', 'client_id', 'client', 'provider')
        depth = 2


class ProviderClients(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            provider = Provider.objects.get(pk=pk)
            serializer = ProviderClientSerializer(
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

        provider = Provider.objects.get(user=request.auth.user)
        client = Client.objects.get(pk=req_body['client_id'])
        
        new_provider_client = ProviderClient()
        new_provider_client.provider = provider
        new_provider_client.client = client

        new_provider_client.save()

        serializer = ProviderClientSerializer(new_provider_client, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            provider_client = ProviderClient.objects.get(pk=pk)
            provider_client.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except provider_client.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientsProviders(ViewSet):
    def list(self, request):
        try:
            client_id = self.request.query_params.get('client_id')

            clients_providers = ProviderClient.objects.filter(client_id=client_id)
            print("clients providers****", len(clients_providers))
            serializer = ProviderClientSerializer(
                clients_providers,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)