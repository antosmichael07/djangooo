from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Studio(models.Model):
    name = models.CharField(max_length=255)
    founded = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        # Validate that founded is not in the future
        if self.founded and self.founded > timezone.localdate():
            raise ValidationError({
                'founded': 'Founded date cannot be in the future.'
            })

    def save(self, *args, **kwargs):
        # Ensure model validation is run before saving
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'studio'
        verbose_name_plural = 'studios'
        indexes = [models.Index(fields=['name'])]


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9-]+$',
                message='Slug must contain only lowercase letters, numbers and hyphens.'
            )
        ]
    )

    def __str__(self):
        return self.name

    def clean(self):
        # Normalize slug to lowercase
        if self.slug:
            self.slug = self.slug.lower()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        indexes = [models.Index(fields=['slug'])]


class Film(models.Model):
    title = models.CharField(max_length=255)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='films')
    genres = models.ManyToManyField(Genre, related_name='films', blank=True)
    release_date = models.DateField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    banner = models.ImageField(
        upload_to='banners/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])]
    )
    synopsis = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        errors = {}
        today = timezone.localdate()

        # release_date cannot be in the future
        if self.release_date and self.release_date > today:
            errors['release_date'] = 'Release date cannot be in the future.'

        # duration must be positive if provided (MinValueValidator also enforces this)
        if self.duration_minutes is not None and self.duration_minutes <= 0:
            errors['duration_minutes'] = 'Duration must be a positive integer.'

        # If studio has a founded date, film's release_date should not be before it
        if self.release_date and self.studio and self.studio.founded:
            if self.release_date < self.studio.founded:
                errors['release_date'] = 'Release date cannot be earlier than the studio founded date.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Run full_clean to ensure model-level validations run before saving
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-release_date', 'title']
        verbose_name = 'film'
        verbose_name_plural = 'films'
        indexes = [models.Index(fields=['release_date']), models.Index(fields=['title'])]
