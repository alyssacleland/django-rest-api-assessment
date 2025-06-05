"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre


class GenreView(ViewSet):
    """Tuna genres view"""

    def list(self, request):
        """Handle GET requests to get all genres

        Returns: 
          Response -- JSON serialized list of genres
        """
        genres = Genre.objects.all()
        serializer = AllGenresSerializer(genres, many=True)
        return Response(serializer.data)


class AllGenresSerializer(serializers.ModelSerializer):
    """JSON Serializer for genres"""
    class Meta:
        model = Genre
        fields = ('id', 'description')
