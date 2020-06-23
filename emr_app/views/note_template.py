from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import NoteTemplate


class NoteTemplateSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = NoteTemplate
        url = serializers.HyperlinkedIdentityField(
            view_name='notetemplate',
            lookup_field='id'
        )
        fields = ('id', 'template')

class NoteTemplates(ViewSet):

    def list(self, request):
        note_templates = NoteTemplate.objects.all()
        serializer = NoteTemplateSerializer(note_templates, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            note_template = NoteTemplate.objects.get(pk=pk)
            serializer = NoteTemplateSerializer(note_template, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_note_template = NoteTemplate()
        new_note_template.template = request.data["template"]
        new_note_template.save()

        serializer = NoteTemplateSerializer(new_note_template, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk=None):
        try:
            note_template = NoteTemplate.objects.get(pk=pk)
            note_template.template = request.data["template"]
            serializer = NoteTemplateSerializer(note_template, context={'request': request}, partial=True)
            note_template.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            
        except note_template.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            note_template = NoteTemplate.objects.get(pk=pk)
            note_template.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except note_template.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
