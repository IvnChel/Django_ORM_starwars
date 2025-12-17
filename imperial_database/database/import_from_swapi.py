# database/import_from_swapi.py
import sys
import os
import django
import requests
from django.db import transaction
import time

# Настраиваем Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imperial_database.settings')
django.setup()

from database.models import Character, Starship

SWAPI_BASE_URL = 'https://swapi.py4e.com/api/'

def parse_numeric(value, default=0):
    """Преобразует строковое значение в число."""
    if not value or value.lower() in ['n/a', 'unknown', 'none']:
        return default
    
    value = value.replace(',', '')
    
    if '-' in value:
        try:
            return int(value.split('-')[0])
        except:
            return default
    
    try:
        return int(float(value)) if '.' in value else int(value)
    except:
        return default

def fetch_item_by_url(url, field='name'):
    """Получает данные по URL и извлекает поле (для планет и видов)."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get(field, 'Unknown')
    except:
        pass
    return 'Unknown'

def fetch_all_from_swapi(endpoint):
    """Получает все данные с пагинированного эндпоинта SWAPI."""
    all_results = []
    next_url = f'{SWAPI_BASE_URL}{endpoint}/'
    
    print(f"Загрузка {endpoint}...")
    
    while next_url:
        try:
            response = requests.get(next_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            all_results.extend(data['results'])
            next_url = data['next']
            
            print(f"  Загружено {len(all_results)} записей", end='\r')
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"\nОшибка при загрузке: {e}")
            break
    
    print(f"\n✓ Загружено всего {len(all_results)} записей {endpoint}")
    return all_results

def import_starships():
    """Импортирует все корабли из SWAPI."""
    ships_data = fetch_all_from_swapi('starships')
    
    created_count = 0
    for ship_data in ships_data:
        try:
            url_parts = ship_data['url'].rstrip('/').split('/')
            swapi_id = url_parts[-1]
            
            if not ship_data.get('name'):
                continue
            
            length = parse_numeric(ship_data.get('length', '0'))
            crew = parse_numeric(ship_data.get('crew', '0'))
            passengers = parse_numeric(ship_data.get('passengers', '0'))
            
            ship, created = Starship.objects.get_or_create(
                swapi_id=swapi_id,
                defaults={
                    'name': ship_data['name'],
                    'model': ship_data.get('model', 'Unknown'),
                    'manufacturer': ship_data.get('manufacturer', 'Unknown'),
                    'length': length,
                    'crew': crew,
                    'passengers': passengers,
                    'starship_class': ship_data.get('starship_class', 'Unknown'),
                }
            )
            
            if created:
                created_count += 1
                
        except Exception as e:
            print(f"Ошибка при импорте корабля: {e}")
    
    return created_count

def import_characters():
    """Импортирует всех персонажей из SWAPI с видами и планетами."""
    people_data = fetch_all_from_swapi('people')
    
    created_count = 0
    for person_data in people_data:
        try:
            url_parts = person_data['url'].rstrip('/').split('/')
            swapi_id = url_parts[-1]
            
            if not person_data.get('name'):
                continue
            
            # Получаем название родной планеты
            homeworld_name = 'Unknown'
            if person_data.get('homeworld'):
                homeworld_name = fetch_item_by_url(person_data['homeworld'], 'name')
            
            # Получаем название вида
            species_name = 'Unknown'
            if person_data.get('species') and person_data['species']:
                # species - это список URL, берем первый
                species_name = fetch_item_by_url(person_data['species'][0], 'name')
            
            height = parse_numeric(person_data.get('height', '0'))
            mass = parse_numeric(person_data.get('mass', '0'))
            
            character, created = Character.objects.get_or_create(
                swapi_id=swapi_id,
                defaults={
                    'name': person_data['name'],
                    'height': height,
                    'mass': mass,
                    'hair_color': person_data.get('hair_color', 'n/a'),
                    'skin_color': person_data.get('skin_color', 'n/a'),
                    'eye_color': person_data.get('eye_color', 'n/a'),
                    'birth_year': person_data.get('birth_year', 'unknown'),
                    'gender': person_data.get('gender', 'n/a'),
                    'homeworld': homeworld_name,
                    'species': species_name,
                }
            )
            
            # Связываем персонажа с кораблями
            if person_data.get('starships'):
                ship_objects = []
                for ship_url in person_data['starships']:
                    try:
                        ship_url_parts = ship_url.rstrip('/').split('/')
                        ship_swapi_id = ship_url_parts[-1]
                        
                        ship = Starship.objects.filter(swapi_id=ship_swapi_id).first()
                        if ship:
                            ship_objects.append(ship)
                    except:
                        continue
                
                if ship_objects:
                    character.starships.set(ship_objects)
            
            if created:
                created_count += 1
                
        except Exception as e:
            print(f"Ошибка при импорте {person_data.get('name', 'Unknown')}: {e}")
    
    return created_count

def run_import():
    """Основная функция для запуска импорта."""
    print("=" * 50)
    print("ИМПОРТ ДАННЫХ ИЗ SWAPI С ВИДАМИ И ПЛАНЕТАМИ")
    print("=" * 50)
    
    choice = input("Очистить существующие данные? (y/n): ").lower()
    if choice == 'y':
        print("Очистка данных...")
        Character.objects.all().delete()
        Starship.objects.all().delete()
        print("Данные очищены.")
    
    try:
        with transaction.atomic():
            print("\n1. Импорт кораблей...")
            ships_count = import_starships()
            
            print("\n2. Импорт персонажей...")
            characters_count = import_characters()
            
            print("\n" + "=" * 50)
            print("ИМПОРТ УСПЕШНО ЗАВЕРШЕН!")
            print("=" * 50)
            print(f"Всего в базе:")
            print(f"  - Кораблей: {Starship.objects.count()}")
            print(f"  - Персонажей: {Character.objects.count()}")
            
            # Показываем примеры
            print("\nПримеры загруженных данных:")
            sample_chars = Character.objects.all()[:3]
            for char in sample_chars:
                print(f"  {char.name}: Вид - {char.species}, Планета - {char.homeworld}")
            
    except Exception as e:
        print(f"\n❌ Ошибка при импорте: {e}")
        print("Импорт отменен.")

if __name__ == "__main__":
    run_import()