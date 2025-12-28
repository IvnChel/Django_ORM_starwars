from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('character/<int:character_id>/', views.character_detail, name='character_detail'),
    path('starship/<int:starship_id>/', views.starship_detail, name='starship_detail'),
]