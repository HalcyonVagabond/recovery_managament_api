"""View module for handling requests about Appointments"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Appointment, Provider, Client


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Appointment
        url = serializers.HyperlinkedIdentityField(
            view_name='appointment',
            lookup_field='id'
        )
        fields = ('id', 'date_time', 'duration', 'provider_id', 'client_id', 'client')
        depth = 2

class Appointments(ViewSet):

    def list(self, request):
        provider = Provider.objects.get(user=request.auth.user)
        appointments = Appointment.objects.filter(provider=provider)
        serializer = AppointmentSerializer(appointments, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_appointment = Appointment()
        print(request)
        provider = Provider.objects.get(user=request.auth.user)
        client = Client.objects.get(id=request.data["client_id"])

        new_appointment.provider = provider
        new_appointment.client = client
        new_appointment.date_time = request.data["date_time"]
        new_appointment.duration = request.data["duration"]

        new_appointment.save()

        serializer = AppointmentSerializer(new_appointment, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            appointment.date_time = request.data["date_time"]
            serializer = AppointmentSerializer(appointment, context={'request': request}, partial=True)
            appointment.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            
        except appointment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            appointment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except appointment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientAppointments(ViewSet):
    def list(self, request):
        print(request.auth)
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True, context={'request': request})
        return Response(serializer.data)