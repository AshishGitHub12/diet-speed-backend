from django.contrib import admin
from .models import FoodItem


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'calories',
        'protein',
        'carbs',
        'fat',
        'quantity',
    )

    search_fields = ('name',)
    ordering = ('name',)