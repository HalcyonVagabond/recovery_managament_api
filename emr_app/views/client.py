from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Client, ProviderClient, Provider


class ClientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Client
        url = serializers.HyperlinkedIdentityField(
            view_name='client',
            lookup_field='id'
        )
        fields = ('url', 'id', 'phone_number', 'address', 'birth_date', 'height', 'weight', 'gender', 'user')
        depth = 1


class Clients(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            serializer = ClientSerializer(
                client, context={
                    'request': request
                }
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(
            clients,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

class UnassignedClients(ViewSet):
    def list(self, request):
        provider = Provider.objects.get(user=request.auth.user)
        providerClients= ProviderClient.objects.filter(provider_id=provider.id)
        p_c_ids = []
        unassignedClients = []
        
        for rel in providerClients:
            p_c_ids.append(rel.client_id)
        clients = Client.objects.all()
        for client in clients:
            if client.id not in p_c_ids:
                unassignedClients.append(client)
        
        print(unassignedClients)
        serializer = ClientSerializer(
            unassignedClients,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)