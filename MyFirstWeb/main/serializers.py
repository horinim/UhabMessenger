from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import UsersList, GroupUser, Post, CommentPost, LikePost


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersList
        fields = ['id', 'username', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        if self.context['request'].method == 'PUT':
            required_fields = ['username', 'email']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(
                        {field: "Это поле обязательно для PUT запроса"}
                    )
        return data

class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = ['id', 'name', 'discription', 'users_list', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
            if self.context['request'].method == 'PUT':
                required_fields = ['name', 'discription', 'users_list']
                for field in required_fields:
                    if field not in data:
                        raise serializers.ValidationError(
                            {field: "Это поле обязательно для PUT запроса"}
                        )
            return data

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author_id', 'group_id', 'content', 'likes_count', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'group_id': {'required': False, 'allow_null': True}
        }

    def validate(self, data):
        if self.context['request'].method == 'PUT':
            required_fields = ['author_id', 'content']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(
                        {field: "Это поле обязательно для PUT запроса"}
                    )
        return data

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentPost
        fields = ['id', 'post_id', 'author_id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'post_id': {'required': True},
            'author_id': {'required': True},
            'text': {'required': True}
        }

    def validate(self, data):
        if self.context['request'].method == 'PUT':
            required_fields = ['author_id', 'text']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(
                        {field: "Это поле обязательно для PUT запроса"}
                    )
        return data

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['id', 'author_id']
        read_only_fields = ['id']
        extra_kwargs = {
            'author_id': {'required': True},
        }

class LikePostRequestSerializer(serializers.Serializer): #Создал для корректного отображения тела запроса
    author_id = serializers.IntegerField()