from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from posts.models import Post, Follow, Group
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class AuthorOrReadOnlyMixin:
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GroupViewSet(AuthorOrReadOnlyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(AuthorOrReadOnlyMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied()
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied()
        super(PostViewSet, self).perform_destroy(instance)


class CommentViewSet(AuthorOrReadOnlyMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post_by_id(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return CommentViewSet.get_post_by_id(self).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=CommentViewSet.get_post_by_id(self)
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied()
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied()
        super(CommentViewSet, self).perform_destroy(instance)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
        # return self.request.user.user_following_these.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
