from rest_framework import serializers

from applications.ad.models import Ad
from applications.comment.serializers import CommentSerializer


class AdSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False},
        }
