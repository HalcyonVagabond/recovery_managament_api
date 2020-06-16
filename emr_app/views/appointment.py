"""View module for handling requests about Appointments"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Appointment


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Appointment
        url = serializers.HyperlinkedIdentityField(
            view_name='appointment',
            lookup_field='id'
        )
        fields = ('id', 'date_time', 'provider_id', 'client_id')
        depth = 2

class Appointments(ViewSet):

    def list(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handle POST operations
    # def create(self, request):
    #     new_appointment = Appointment()
    #     print("REQUESTDATA", new_appointment)

    #     customer = Customer.objects.get(user=request.auth.user)

    #     new_Appointment.title = request.data["title"]
    #     new_Appointment.customer = customer
    #     new_Appointment.description = request.data["description"]
    #     new_Appointment.quantity = request.data["quantity"]
    #     new_Appointment.location = request.data["location"]
    #     new_Appointment.image_path = request.data["image_path"]
    #     new_Appointment.created_at = request.data["created_at"]
    #     new_Appointment.Appointment_type = Appointment
    #     print("REQUESTDATA", request.data)

    #     print("NEW_Appointment", new_appointment)
    #     new_appointment.save()

    #     serializer = AppointmentSerializer(new_appointment, context={'request': request})
    #     return Response(serializer.data)

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