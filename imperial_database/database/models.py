from django.db import models


class Starship(models.Model):
    """Модель космического корабля"""
    name = models.CharField(max_length=100, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель")
    manufacturer = models.CharField(max_length=100, verbose_name="Производитель")
    length = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Длина (м)")
    crew = models.IntegerField(verbose_name="Экипаж")
    passengers = models.IntegerField(verbose_name="Пассажиры")
    starship_class = models.CharField(max_length=100, verbose_name="Класс корабля")
    swapi_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="ID в SWAPI")
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Космический корабль"
        verbose_name_plural = "Космические корабли"

class Character(models.Model):
    """Модель персонажа Звёздных войн"""
    
    # Выбор пола
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('n/a', 'Не указан'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя")
    height = models.IntegerField(verbose_name="Рост (см)")
    mass = models.IntegerField(verbose_name="Вес (кг)")
    hair_color = models.CharField(max_length=50, verbose_name="Цвет волос")
    skin_color = models.CharField(max_length=50, verbose_name="Цвет кожи")
    eye_color = models.CharField(max_length=50, verbose_name="Цвет глаз")
    birth_year = models.CharField(max_length=20, verbose_name="Год рождения")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Пол")
    homeworld = models.CharField(max_length=100, verbose_name="Родная планета")
    species = models.CharField(max_length=100, verbose_name="Вид")
    swapi_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="ID в SWAPI")
    
    # Связь с кораблём (у персонажа может быть несколько кораблей)
    starships = models.ManyToManyField(Starship, related_name='pilots', verbose_name="Корабли")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"
# Create your models here.
