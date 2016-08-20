from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Photo, Comment, Like, Dislike


class UserSerializer(serializers.ModelSerializer):
    photos = serializers.HyperlinkedIdentityField(view_name='userphoto-list', lookup_field='username')
    avatar = serializers.ImageField(default='./no_avatar.gif')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'photos', 'avatar')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo

    user = UserSerializer(required=False)
    image = serializers.ImageField()
    data = serializers.DateTimeField(format='%d %B %Y')
    comment_count = serializers.IntegerField(default=0)
    likes = serializers.IntegerField(default=0)
    dislikes = serializers.IntegerField(default=0)


def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(PhotoSerializer, self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

    image = PhotoSerializer(required=False)
    user = UserSerializer(required=False)
    comment = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=100)
    data = serializers.DateTimeField(format='%d %B')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(CommentSerializer, self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['image'] + ['user']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like

    image = serializers.IntegerField()
    username = serializers.CharField(max_length=100)


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike

    image = serializers.IntegerField()
    username = serializers.CharField(max_length=100)