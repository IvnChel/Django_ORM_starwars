# database/admin.py
from django.contrib import admin
from .models import Character, Starship

@admin.register(Starship)
class StarshipAdmin(admin.ModelAdmin):
    """Настройка отображения кораблей в админке"""
    list_display = ('name', 'model', 'manufacturer', 'starship_class')
    list_filter = ('starship_class', 'manufacturer')
    search_fields = ('name', 'model')
    ordering = ('name',)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Настройка отображения персонажей в админке"""
    list_display = ('name', 'species', 'homeworld', 'gender')
    list_filter = ('species', 'gender', 'homeworld')
    search_fields = ('name', 'species', 'homeworld')
    filter_horizontal = ('starships',)  # Удобный выбор кораблей
    ordering = ('name',)