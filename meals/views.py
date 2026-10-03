from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import date

from .models import MealEntry, FoodItem, WaterLog, MealCompletion
from .serializers import MealEntrySerializer, FoodItemSerializer
from profiles.models import UserProfile

DEFAULT_CALORIE_GOAL = 2000
WATER_TARGET = 8

# Static per-meal metadata (icon/time/share of daily calories). Not stored in
# the DB since it's the same for every user — only the numbers driven by it
# (target_calories) vary per user via calorie_goal.
MEAL_META = {
    "breakfast": {"label": "Breakfast", "icon": "sunny-outline",        "time": "08:00 AM", "split": 0.25},
    "lunch":     {"label": "Lunch",     "icon": "partly-sunny-outline", "time": "01:00 PM", "split": 0.35},
    "snack":     {"label": "Snack",     "icon": "cafe-outline",         "time": "04:00 PM", "split": 0.10},
    "dinner":    {"label": "Dinner",    "icon": "moon-outline",         "time": "08:00 PM", "split": 0.30},
}


def _macro_targets(calorie_goal):
    """Standard macro split (~27% protein / 43% carbs / 30% fat by calories).
    Adjust these ratios if you want something more personalized later."""
    return {
        "protein": round(calorie_goal * 0.27 / 4),
        "carbs":   round(calorie_goal * 0.43 / 4),
        "fat":     round(calorie_goal * 0.30 / 9),
    }


def _ai_tip(macros):
    """Rule-based tip (not a real AI call) based on whichever macro has the
    biggest gap to its target."""
    gaps = {
        "protein": macros["protein"]["target"] - macros["protein"]["consumed"],
        "carbs":   macros["carbs"]["target"] - macros["carbs"]["consumed"],
        "fat":     macros["fat"]["target"] - macros["fat"]["consumed"],
    }
    biggest = max(gaps, key=gaps.get)
    if gaps[biggest] <= 0:
        return "Great job! You're on track with all your macros today."

    suggestions = {
        "protein": "a handful of nuts, Greek yogurt, or a boiled egg",
        "carbs":   "a banana, some oats, or a slice of whole-grain bread",
        "fat":     "some avocado, nuts, or a drizzle of olive oil",
    }
    return f"You're {round(gaps[biggest])}g short on {biggest} today. Try adding {suggestions[biggest]} to hit your target!"


class DietView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        entry_date = request.GET.get('date') or date.today().isoformat()

        try:
            profile = UserProfile.objects.get(user=user)
            calorie_goal = profile.calorie_goal or DEFAULT_CALORIE_GOAL
        except UserProfile.DoesNotExist:
            calorie_goal = DEFAULT_CALORIE_GOAL

        targets = _macro_targets(calorie_goal)

        entries = list(MealEntry.objects.filter(user=user, date=entry_date))
        completions = {
            c.meal_type: c.completed
            for c in MealCompletion.objects.filter(user=user, date=entry_date)
        }

        consumed_protein = sum(e.protein for e in entries)
        consumed_carbs = sum(e.carbs for e in entries)
        consumed_fat = sum(e.fat for e in entries)
        consumed_calories = sum(e.calories for e in entries)

        meals = []
        for meal_type, meta in MEAL_META.items():
            meal_entries = [e for e in entries if e.meal_type == meal_type]
            meals.append({
                "type": meal_type,
                "label": meta["label"],
                "icon": meta["icon"],
                "time": meta["time"],
                "target_calories": round(calorie_goal * meta["split"]),
                "completed": completions.get(meal_type, False),
                "items": MealEntrySerializer(meal_entries, many=True).data,
            })

        try:
            water_glasses = WaterLog.objects.get(user=user, date=entry_date).glasses
        except WaterLog.DoesNotExist:
            water_glasses = 0

        macros = {
            "protein": {"target": targets["protein"], "consumed": round(consumed_protein)},
            "carbs":   {"target": targets["carbs"],   "consumed": round(consumed_carbs)},
            "fat":     {"target": targets["fat"],     "consumed": round(consumed_fat)},
        }

        return Response({
            "date": entry_date,
            "calories_target": calorie_goal,
            "calories_consumed": consumed_calories,
            "macros": macros,
            "meals": meals,
            "water_glasses": water_glasses,
            "water_target": WATER_TARGET,
            "ai_tip": _ai_tip(macros),
        })


class MealItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = {**request.data}
        payload.setdefault('date', date.today().isoformat())

        # If a food_item id was passed, copy its nutrition onto the entry
        # (unless the client already supplied overrides).
        food_item_id = payload.get('food_item')
        if food_item_id:
            try:
                food = FoodItem.objects.get(id=food_item_id)
                payload.setdefault('name', food.name)
                payload.setdefault('calories', food.calories)
                payload.setdefault('protein', food.protein)
                payload.setdefault('carbs', food.carbs)
                payload.setdefault('fat', food.fat)
                payload.setdefault('quantity', food.quantity)
            except FoodItem.DoesNotExist:
                pass

        serializer = MealEntrySerializer(data=payload)
        if serializer.is_valid():
            entry = serializer.save(user=request.user)
            return Response(MealEntrySerializer(entry).data, status=201)

        return Response(serializer.errors, status=400)


class MealItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            entry = MealEntry.objects.get(id=pk, user=request.user)
            entry.delete()
            return Response({"message": "Deleted"}, status=200)
        except MealEntry.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


class FoodSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q', '')
        foods = FoodItem.objects.all()
        if query:
            foods = foods.filter(name__icontains=query)
        return Response(FoodItemSerializer(foods[:20], many=True).data)


class WaterLogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        entry_date = request.data.get('date') or date.today().isoformat()
        glasses = request.data.get('glasses')

        if glasses is None:
            return Response({"glasses": "This field is required."}, status=400)
        try:
            glasses = max(0, int(glasses))
        except (TypeError, ValueError):
            return Response({"glasses": "Must be a whole number."}, status=400)

        water, _ = WaterLog.objects.update_or_create(
            user=user, date=entry_date, defaults={"glasses": glasses}
        )
        return Response({"glasses": water.glasses})


class MealCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meal_type):
        user = request.user
        entry_date = request.data.get('date') or date.today().isoformat()

        completion, _ = MealCompletion.objects.get_or_create(
            user=user, date=entry_date, meal_type=meal_type
        )
        completion.completed = not completion.completed
        completion.save()

        return Response({"meal_type": meal_type, "completed": completion.completed})