from django.db import models

from .constants import CHARFIELD_MAX_LENGTH, SLUGFIELD_MAX_LENGTH


class NameModel(models.Model):
    """Абстрактная модель с общим полем name."""

    name = models.CharField('Название', max_length=CHARFIELD_MAX_LENGTH)

    class Meta:
        abstract = True
        ordering = ('name',)


class SlugModel(models.Model):
    """Абстрактная модель с общим полем slug."""

    slug = models.SlugField(
        'Слаг', unique=True, max_length=SLUGFIELD_MAX_LENGTH)

    class Meta:
        abstract = True


class TextPubdateModel(models.Model):
    """Абстрактная модель с общими полями: text, pub_date."""

    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        abstract = True
