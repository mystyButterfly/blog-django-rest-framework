from rest_framework import serializers
from .models import Post, Author, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        author = Author.objects.create(user=user, name=user.username)
        author.save()
        return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'body', 'author']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # Nested serialization of Author and Post
    # author = AuthorSerializer()
    # post = PostSerializer()
    
    class Meta:
        model = Comment
        fields = '__all__'
