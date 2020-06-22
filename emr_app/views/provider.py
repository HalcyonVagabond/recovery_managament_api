from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Provider


class ProviderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Provider
        url = serializers.HyperlinkedIdentityField(
            view_name='provider',
            lookup_field='id'
        )
        fields = ('id', 'phone_number')
        depth = 1


class Providers(ViewSet):

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

        providers = Provider.objects.all()
        serializer = ProviderSerializer(
            providers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)