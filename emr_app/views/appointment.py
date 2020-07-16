"""View module for handling requests about Appointments"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Appointment, Provider, Client
from ..mail_test import AppointmentEmail
import copy
import random
import string

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Appointment
        url = serializers.HyperlinkedIdentityField(
            view_name='appointment',
            lookup_field='id'
        )
        fields = ('id', 'date_time', 'duration', 'provider_id', 'client_id', 'client', 'appointment_url')
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
        provider = Provider.objects.get(user=request.auth.user)
        client = Client.objects.get(id=request.data["client_id"])

        new_appointment.provider = provider
        new_appointment.client = client
        new_appointment.date_time = request.data["date_time"]
        new_appointment.duration = request.data["duration"]
        new_appointment.virtual_boolean = True
        if new_appointment.virtual_boolean == True:
            def random_string(stringLength=20):
                letters = string.hexdigits
                return ''.join(random.choice(letters) for i in range(stringLength))
            new_appointment.appointment_url = f'telehealth.evolvingrecovery.com/{random_string()}'
        new_appointment.save()
        AppointmentEmail().created_appointment(new_appointment)
        
        serializer = AppointmentSerializer(new_appointment, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            provider = Provider.objects.get(user=request.auth.user)
            client = Client.objects.get(id=request.data["client_id"])
            appointment.duration = request.data["duration"]
            appointment.date_time = request.data["date_time"]
            serializer = AppointmentSerializer(appointment, context={'request': request}, partial=True)
            appointment.save()
            AppointmentEmail().edited_appointment(appointment)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            
        except appointment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        appointment = Appointment.objects.get(pk=pk)
        # AppointmentEmail().canceled_appointment(appointment)
        try:
            appointment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except appointment.DoesNotExist as ex:
            return Response({'message appointment does not exist': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message exception': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientAppointments(ViewSet):
    def list(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True, context={'request': request})
        return Response(serializer.data)

class ReminderEmail(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            AppointmentEmail().reminder_email(appointment)
            serializer = AppointmentSerializer(appointment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    