"""View module for handling requests about songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song


class SongView(ViewSet):
    """Tuna songs view"""

    def list(self, request):
        """Handle GET requests to get all songs

        Returns: 
          Response -- JSON serialized list of songs
        """
        songs = Song.objects.all()
        serializer = AllSongsSerializer(songs, many=True)
        return Response(serializer.data)

    # TODO: within list method: this filter isn't required but i'm gonna do it for practice. FILTER SONGS BY ARTIST IF PROVIDED. see events view for help.


class AllSongsSerializer(serializers.ModelSerializer):
    """JSON Serializer for artists"""
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')
