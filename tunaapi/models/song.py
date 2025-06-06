from django.db import models
from .artist import Artist


class Song(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.CharField(max_length=50)
    length = models.PositiveIntegerField()


# related_name: This is used to specify the name of the reverse relation from the Artist model to the Song model. without this, the default would be 'song_set'
