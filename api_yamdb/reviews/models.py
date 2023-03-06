from django.db import models

from .validators import year_validator


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        unique=True,
    )

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    year = models.PositiveSmallIntegerField(
        validators=[year_validator],
        verbose_name='Дата выхода',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta():
        ordering = ('year',)
        verbose_name = 'title'
        verbose_name_plural = 'titles'

