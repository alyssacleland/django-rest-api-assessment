"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, Song
# from tunaapi.views.song import AllSongsSerializer


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

    def retrieve(self, request, pk):
        """Handle GET requests for a single genre

        Returns:
          Response -- JSON serialized genre with its songs
        """
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = SingleGenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ handle POST requests for gneres"""
        genre = Genre.objects.create(
            description=request.data["description"]
        )
        serializer = AllGenresSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """handle PUT requests for genres"""
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()
        serializer = AllGenresSerializer(genre)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """ handle delete requests for single genre"""
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class AllGenresSerializer(serializers.ModelSerializer):
    """JSON Serializer for genres"""
    class Meta:
        model = Genre
        fields = ('id', 'description')


class SingleGenreSerializer(serializers.ModelSerializer):
    """JSON Serializer for a single genre including its songs"""
    songs = serializers.SerializerMethodField()

    def get_songs(self, obj):
        # Reverse lookup through join table
        songs = Song.objects.filter(songgenre__genre=obj)
        return AllSongsSerializer(songs, many=True).data

    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')


# not best practice but to avoid circular imports, we define AllSongsSerializer here. really i should put all the serializers in a separate file instead but it's 2 am and i'm tired
class AllSongsSerializer(serializers.ModelSerializer):
    """JSON Serializer for artists"""
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')
