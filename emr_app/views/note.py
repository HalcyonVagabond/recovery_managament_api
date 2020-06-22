from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Note, Provider, Client, NoteTemplate

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Note
        url = serializers.HyperlinkedIdentityField(
            view_name='note',
            lookup_field='id'
        )
        fields = ('id', 'date_time', 'client_id', 'client', 'provider_id', 'provider', 'content', 'note_template')
        depth = 2

class Notes(ViewSet):

    def list(self, request):
        client_id = self.request.query_params.get('client_id')

        notes = Note.objects.filter(client_id=client_id)
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            notes = Note.objects.filter(pk=pk)
            serializer = NoteSerializer(notes, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_note = Note()
        print("Request Data!", request.data)
        provider = Provider.objects.get(user=request.auth.user)
        client = Client.objects.get(id=request.data["client_id"])
        note_template = NoteTemplate.objects.get(id=request.data["note_template_id"])
        
        new_note.provider = provider
        new_note.client = client
        new_note.note_template = note_template
        new_note.content = request.data["content"]
        new_note.date_time = request.data["date_time"]

        new_note.save()

        serializer = NoteSerializer(new_note, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk=None):
        try:
            note = Note.objects.get(pk=pk)
            note.date_time = request.data["date_time"]
            serializer = NoteSerializer(note, context={'request': request}, partial=True)
            note.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            
        except note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            note = Note.objects.get(pk=pk)
            note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientNotes(ViewSet):
    def list(self, request):
        print(request.auth)
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data)