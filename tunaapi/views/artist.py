"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist
from django.db.models import Count
from tunaapi.views.song import AllSongsSerializer


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

    def retrieve(self, request, pk):
        try:
            # Count is a python fx that returns the number of times an object appears in a list.
            # Annotate is a method that allows you to add a new field to the queryset that is calculated based on the existing fields.
            # Count('songs') uses the reverse relationship from Artist to Song (thanks to the foreign key artist on Song).
            artist = Artist.objects.annotate(
                song_count=Count('songs')).get(pk=pk)
            serializer = SingleArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"]
        )
        serializer = AllArtistsSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """ handle PUT requests for artists"""
        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]

        artist.save()
        serializer = AllArtistsSerializer(artist)
        return Response(serializer.data)


class AllArtistsSerializer(serializers.ModelSerializer):
    """JSON Serializer for artists"""
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')


class SingleArtistSerializer(serializers.ModelSerializer):
    """JSON Serializer for a single artist including their songs"""
    songs = AllSongsSerializer(many=True, read_only=True)
    song_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
