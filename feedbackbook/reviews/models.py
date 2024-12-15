from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import NameModel, SlugModel, TextPubdateModel
from core.validators import year_validator
from core.constants import (MIN_SCORE,
                            MAX_SCORE,
                            USER_CHARFIELD_MAX_LENGTH,
                            EMAILFIELD_MAX_LENGTH,
                            USER_ROLES,
                            USER,
                            MODERATOR,
                            ADMIN)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    USER = USER
    MODERATOR = MODERATOR
    ADMIN = ADMIN

    username = models.CharField(
        'Имя пользователя',
        unique=True,
        max_length=USER_CHARFIELD_MAX_LENGTH)
    email = models.EmailField(
        'Почта',
        unique=True,
        blank=False,
        max_length=EMAILFIELD_MAX_LENGTH)
    first_name = models.CharField(
        'Имя',
        blank=True,
        null=True,
        max_length=USER_CHARFIELD_MAX_LENGTH)
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        null=True,
        max_length=USER_CHARFIELD_MAX_LENGTH)
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True)
    role = models.CharField(
        'Роль пользователя',
        default=USER,
        choices=USER_ROLES,
        max_length=USER_CHARFIELD_MAX_LENGTH)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=USER_CHARFIELD_MAX_LENGTH)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_staff
            or self.is_superuser)

    def __str__(self):
        return self.username


class Category(NameModel, SlugModel):
    """Модель категорий."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(NameModel, SlugModel):
    """Модель жанров."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(NameModel):
    """Модель произведений."""

    year = models.SmallIntegerField(
        'Год выпуска',
        validators=(year_validator,))
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True)
    genre = models.ManyToManyField(Genre)

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name', 'year', 'category')

    def __str__(self):
        return self.name


class Review(TextPubdateModel):
    """Модель отзывов."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение')
    score = models.PositiveIntegerField(
        validators=(MinValueValidator(MIN_SCORE, f'Минимум  {MIN_SCORE}'),
                    MaxValueValidator(MAX_SCORE, f'Максимум {MAX_SCORE}')),
        verbose_name='Оценка произведения')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (models.UniqueConstraint(
            fields=('author', 'title'),
            name='unique_author_title'),)

    def __str__(self):
        return f'Отзыв к произведению "{self.title.name}"'


class Comment(TextPubdateModel):
    """Модель комментариев."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
