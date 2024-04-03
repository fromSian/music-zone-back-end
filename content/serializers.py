from rest_framework import serializers
from .models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "create_time": {"read_only": True},
            "update_time": {"read_only": True},
        }
