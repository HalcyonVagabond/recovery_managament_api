from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Client


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
        print(request)
        clients = Client.objects.all()
        serializer = ClientSerializer(
            clients,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)