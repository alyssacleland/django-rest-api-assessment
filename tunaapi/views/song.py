"""View module for handling requests about songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Genre, Artist
from tunaapi.views.genre import AllGenresSerializer


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

    def retrieve(self, request, pk):
        """ handle get requests for a single song 
        """
        try:
            song = Song.objects.get(pk=pk)
            serializer = SingleSongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ handle post requests """
        artist = Artist.objects.get(pk=request.data["artist_id"])
        song = Song.objects.create(
            title=request.data["title"],
            artist_id=artist.id,
            album=request.data["album"],
            length=request.data["length"]
        )
        serializer = AllSongsSerializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """ handle put requests for songs"""

        # artist = Artist.objects.get(pk=request.data["artist_id"])..... don't need this because ticket wants the id, not the obj
        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        # song.artist_id = artist.id
        song.artist_id = request.data["artist_id"]
        song.album = request.data["album"]
        song.length = request.data["length"]

        song.save()
        serializer = AllSongsSerializer(song)
        return Response(serializer.data)


class AllSongsSerializer(serializers.ModelSerializer):
    """JSON Serializer for artists"""
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')


class SingleSongSerializer(serializers.ModelSerializer):
    """JSON Serializer for a single song"""

    # SerializerMethodField is used to create a custom field in the serializer that is not directly part of the model.
    # It allows you to define a method that will be called to get the value for that field. the method must be named get_<field_name>.
    genres = serializers.SerializerMethodField()

    def get_genres(self, obj):
        # Apparently obj is the song being passed to the serializer behind the scenes instead of explicity passing it as an argument ahhh why
        # also fx has to be named get_<field_name> for it to work. drf
        """Get the genres for the song"""
        # Return all Genre objects that are linked to the given song (obj) through SongGenre records where SongGenre.song matches obj and SongGenre.genre_id matches Genre.id via the foreign key relationship.
        genres = Genre.objects.filter(songgenre__song=obj)
        return AllGenresSerializer(genres, many=True).data

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album',
                  'length', 'genres')
        depth = 1  # This will include the related artist information in the serialized data
