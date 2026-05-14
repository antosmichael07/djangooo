from django.db import models


class Studio(models.Model):
    name = models.CharField(max_length=255)
    founded = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=255)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='films')
    genres = models.ManyToManyField(Genre, related_name='films', blank=True)
    release_date = models.DateField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    synopsis = models.TextField(blank=True)

    def __str__(self):
        return self.title
