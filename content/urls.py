from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("artists", views.ArtistViewSet, basename="artists")

urlpatterns = []
urlpatterns = urlpatterns + router.urls
