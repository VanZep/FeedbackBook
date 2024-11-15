from django.conf import settings
from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (viewsets, filters, permissions, status)
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import CustomUser, Category, Genre, Title, Review
from .filters import TitleFilter
from .mixins import ListCreateDestroy
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          SignUpSerializer,
                          CustomTokenObtainPairSerializer,
                          UserSerializer,
                          ProfileSerializer,
                          TitlesCreateSerializer)
from .permissions import (IsAdminOrReadOnlyPermission,
                          IsAuthorOrAdminPermission,
                          IsAdminPermission)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    """Функция представления регистрации."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user, _ = CustomUser.objects.get_or_create(
        username=username, email=email)

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        subject='YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.EMAIL_ADMIN,
        recipient_list=(email,))
    return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Представление получения токена."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, * args, ** kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.validated_data['username']
        confirmation_code = request.validated_data['confirmation_code']
        user = get_object_or_404(CustomUser, username=username)

        if confirmation_code != user.confirmation_code:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Представление пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission, )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^role', '^username')
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=ProfileSerializer)
    def set_profile(self, request, pk=None):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminOrReadOnlyPermission, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitlesCreateSerializer
        return TitleSerializer


class CategoryViewSet(ListCreateDestroy):
    """Представление категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroy):
    """Представление жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление отзывов."""

    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthorOrAdminPermission, )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Представление комментариев."""

    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthorOrAdminPermission, )

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
