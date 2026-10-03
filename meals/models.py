from django.db import models
from django.contrib.auth.models import User
from datetime import date as date_cls


class FoodItem(models.Model):
    """Reference nutrition database used for food search / quick-add."""

    name = models.CharField(max_length=150, unique=True)
    calories = models.PositiveIntegerField()
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    quantity = models.CharField(max_length=50, default="1 serving")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MealEntry(models.Model):

    # NOTE: this uses "snack" (singular) — if you kept the earlier simpler
    # meals app with "snacks" (plural), this is a breaking rename. Fine for
    # a fresh feature with no real logged data yet; flagging just in case.
    MEAL_TYPE_CHOICES = (
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("snack", "Snack"),
        ("dinner", "Dinner"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_entries")
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True)

    # Macros are copied onto the entry at log time (not read live from
    # FoodItem) so a later edit to the reference database doesn't silently
    # rewrite someone's food history.
    name = models.CharField(max_length=150)
    calories = models.PositiveIntegerField()
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    quantity = models.CharField(max_length=50, blank=True)

    date = models.DateField(default=date_cls.today)
    time = models.TimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["time"]

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.calories} kcal) on {self.date}"


class WaterLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="water_logs")
    date = models.DateField(default=date_cls.today)
    glasses = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["user", "date"]

    def __str__(self):
        return f"{self.user.username} - {self.glasses} glasses on {self.date}"


class MealCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_completions")
    date = models.DateField(default=date_cls.today)
    meal_type = models.CharField(max_length=10, choices=MealEntry.MEAL_TYPE_CHOICES)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "date", "meal_type"]

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} on {self.date}: {self.completed}"