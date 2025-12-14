# database/views.py
from django.shortcuts import render, get_object_or_404
from .models import Character, Starship

def index(request):
    """Главная страница со всеми персонажами"""
    characters = Character.objects.all().order_by('name')
    return render(request, 'database/index.html', {'characters': characters})

def character_detail(request, character_id):
    """Страница конкретного персонажа"""
    character = get_object_or_404(Character, id=character_id)
    return render(request, 'database/character.html', {'character': character})

def starship_detail(request, starship_id):
    """Страница конкретного корабля"""
    starship = get_object_or_404(Starship, id=starship_id)
    return render(request, 'database/starship.html', {'starship': starship})
