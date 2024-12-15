from django.urls import path, include
from rest_framework import routers

from .views import (signup,
                    CategoryViewSet,
                    CommentViewSet,
                    GenreViewSet,
                    CustomTokenObtainPairView,
                    ReviewViewSet,
                    TitleViewSet,
                    UserViewSet,
                    )


app_name = 'api'


router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token'),
]
