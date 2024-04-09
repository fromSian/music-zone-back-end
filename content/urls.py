from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("artists", views.ArtistViewSet, basename="artists")

router.register("albums", views.AlbumViewSet, basename="albums")


router.register("songs", views.SongViewSet, basename="songs")


router.register("playlists", views.PlaylistViewSet, basename="playlists")

router.register("play-record", views.PlayRecordViewSet, basename="play record")

urlpatterns = [
    path("search/", views.search, name="search"),
    path("clear/", views.clear, name="clear"),
    path("get_love_playlist/", views.get_love_playlist, name="get_love_playlist"),
]
urlpatterns = urlpatterns + router.urls
