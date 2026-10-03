from django.core.management.base import BaseCommand
from meals.models import FoodItem

FOODS = [
    {"name": "Apple",          "calories": 95,  "protein": 0,  "carbs": 25, "fat": 0,  "quantity": "1 medium"},
    {"name": "Banana",         "calories": 90,  "protein": 1,  "carbs": 23, "fat": 0,  "quantity": "1 medium"},
    {"name": "Boiled egg",     "calories": 78,  "protein": 6,  "carbs": 1,  "fat": 5,  "quantity": "1 piece"},
    {"name": "Brown rice",     "calories": 210, "protein": 5,  "carbs": 44, "fat": 2,  "quantity": "1 cup"},
    {"name": "Chicken breast", "calories": 165, "protein": 31, "carbs": 0,  "fat": 4,  "quantity": "100g"},
    {"name": "Greek yogurt",   "calories": 100, "protein": 17, "carbs": 6,  "fat": 1,  "quantity": "1 cup"},
    {"name": "Oats",           "calories": 150, "protein": 5,  "carbs": 27, "fat": 3,  "quantity": "1/2 cup"},
    {"name": "Paneer",         "calories": 265, "protein": 18, "carbs": 3,  "fat": 20, "quantity": "100g"},
    {"name": "Roti",           "calories": 104, "protein": 3,  "carbs": 18, "fat": 3,  "quantity": "1 piece"},
    {"name": "Salmon",         "calories": 208, "protein": 20, "carbs": 0,  "fat": 13, "quantity": "100g"},
    {"name": "Sweet potato",   "calories": 86,  "protein": 2,  "carbs": 20, "fat": 0,  "quantity": "100g"},
    {"name": "Whole milk",     "calories": 149, "protein": 8,  "carbs": 12, "fat": 8,  "quantity": "1 cup"},
    {"name": "Almonds",        "calories": 164, "protein": 6,  "carbs": 6,  "fat": 14, "quantity": "28g"},
    {"name": "Dal (lentils)",  "calories": 230, "protein": 18, "carbs": 40, "fat": 1,  "quantity": "1 cup"},
    {"name": "Chapati",        "calories": 120, "protein": 4,  "carbs": 20, "fat": 3,  "quantity": "1 piece"},
]


class Command(BaseCommand):
    help = "Seed the FoodItem reference table used by food search / quick-add."

    def handle(self, *args, **options):
        created = 0
        for food in FOODS:
            _, was_created = FoodItem.objects.get_or_create(name=food["name"], defaults=food)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new food item(s) ({len(FOODS)} checked)."))