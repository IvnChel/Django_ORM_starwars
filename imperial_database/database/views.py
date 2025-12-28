from django.shortcuts import render, get_object_or_404
from .models import Character, Starship

def index(request):
    characters = Character.objects.all().order_by('name')
    return render(request, 'database/index.html', {'characters': characters})

def character_detail(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    return render(request, 'database/character.html', {'character': character})

def starship_detail(request, starship_id):
    starship = get_object_or_404(Starship, id=starship_id)
    return render(request, 'database/starship.html', {'starship': starship})