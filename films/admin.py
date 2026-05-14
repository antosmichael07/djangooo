from django.contrib import admin
from django.utils.html import format_html
from .models import Film, Studio, Genre


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'founded', 'country')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('banner_tag', 'title', 'studio', 'release_date', 'duration_minutes')
    list_filter = ('studio', 'genres')
    search_fields = ('title',)
    def banner_tag(self, obj):
        if obj.banner:
            return format_html('<img src="{}" style="height:50px;object-fit:cover;"/>', obj.banner.url)
        return '-'
    banner_tag.short_description = 'Banner'
