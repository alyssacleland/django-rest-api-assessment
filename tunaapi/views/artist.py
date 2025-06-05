"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist


class ArtistView(ViewSet):
    """Tuna artists view"""

    def list(self, request):
        """Handle GET requests to get all artists

        Returns: 
          Response -- JSON serialized list of artists
        """
        artists = Artist.objects.all()
        serializer = AllArtistsSerializer(artists, many=True)
        return Response(serializer.data)


class AllArtistsSerializer(serializers.ModelSerializer):
    """JSON Serializer for artists"""
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')
