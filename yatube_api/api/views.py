from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import get_object_or_404

from posts.models import Post, Follow, Group
from .permissions import AuthorOrReadOnly, ReadOnly
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_post_by_id(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return CommentViewSet.get_post_by_id(self).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=CommentViewSet.get_post_by_id(self)
        )


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
        # return self.request.user.user_following_these.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
