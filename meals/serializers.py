from rest_framework import serializers
from .models import MealEntry, FoodItem


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ["id", "name", "calories", "protein", "carbs", "fat", "quantity"]


class MealEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealEntry
        fields = [
            "id", "meal_type", "food_item", "name", "calories",
            "protein", "carbs", "fat", "quantity", "date", "time",
        ]
        read_only_fields = ["id", "time"]

    def validate_calories(self, value):
        if value <= 0:
            raise serializers.ValidationError("Calories must be a positive number.")
        return value