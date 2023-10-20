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


# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(  # type: ignore[var-annotated]
#         slug_field='username', read_only=True)

#     class Meta:
#         model = Comment
#         fields = ('id', 'author', 'post', 'text', 'created')
#         read_only_fields = ('post',)


# class PostSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(  # type: ignore[var-annotated]
#         slug_field='username', read_only=True)

#     class Meta:
#         model = Post
#         fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('id', 'title', 'slug', 'description')
