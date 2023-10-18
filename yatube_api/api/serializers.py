from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)  # type: ignore[var-annotated]  # noqa: E501

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(  # type: ignore[var-annotated]
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
