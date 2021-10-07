from rest_framework import serializers
from .models import BookMark


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = [
            "id",
            "title",
            "url",
            "create_at",
            "is_public",
            "user"
        ]
        read_only_fields = ('create_at', 'user')
