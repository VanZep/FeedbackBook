import re
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import (Category,
                            Comment,
                            Genre,
                            Review,
                            Title,
                            CustomUser)
from core.constants import (EMAILFIELD_MAX_LENGTH,
                            USER_CHARFIELD_MAX_LENGTH,
                            USER_ROLES,
                            USER)
from core.validators import (username_validator,
                             year_validator,
                             CustomValidation)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации."""

    username = serializers.CharField(max_length=USER_CHARFIELD_MAX_LENGTH)
    email = serializers.EmailField(max_length=EMAILFIELD_MAX_LENGTH)

    def validate_username(self, value):
        username_validator(value)
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if (CustomUser.objects.filter(username=username).exists()
                and CustomUser.objects.get(username=username).email != email):
            raise serializers.ValidationError(
                'Такая почта уже существует')
        if (CustomUser.objects.filter(email=email).exists()
                and CustomUser.objects.get(email=email).username != username):
            raise serializers.ValidationError(
                'Такое имя пользователя уже существует')

        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор получения токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            return username
        raise CustomValidation('Пользователь не найден',
                               status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели CustomUser."""

    role = serializers.ChoiceField(choices=USER_ROLES, default=USER)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=USER_CHARFIELD_MAX_LENGTH,
        validators=(UniqueValidator(queryset=CustomUser.objects.all()), ))
    email = serializers.EmailField(
        max_length=EMAILFIELD_MAX_LENGTH,
        validators=(UniqueValidator(queryset=CustomUser.objects.all()), ))

    class Meta:
        model = CustomUser
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    def validate_username(self, username):
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError(
                'Недопутимые символы в username.')
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено!')
        return username


class ProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id', )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['name'],
                message=('Такая категория уже существует!'), )]


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id', )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=['name'],
                message=('Такая категория уже существует!'), )]


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year_validator(value)
        return value


class TitlesCreateSerializer(TitleSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),)
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(title_id=title_id,
                                 author_id=user.id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение. '
                'Можете его отредактировать.')

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)
