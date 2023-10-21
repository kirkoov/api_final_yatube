from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet


app_name = 'api'


v1_router = DefaultRouter()
v1_router.register('v1/posts', PostViewSet)
v1_router.register(
    r'v1/posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment-noquery-viewset')
v1_router.register('v1/groups', GroupViewSet)
v1_router.register(
    'v1/follow', FollowViewSet, basename='following')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
