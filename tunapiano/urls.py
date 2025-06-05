"""tunapiano URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from tunaapi.views import SongView, GenreView, ArtistView


# router.register variables: Used with viewsets to automatically generate multiple RESTful routes.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'songs', SongView, 'song')
router.register(r'artists', ArtistView, 'artist')
router.register(r'genres', GenreView, 'genre')

# path(...): Used for explicitly defining a route to a view function or class.
urlpatterns = [
    path('admin/', admin.site.urls),
    # add router variables (above) to url patterns
    path('', include(router.urls)),
]
