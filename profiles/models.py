from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    HEIGHT_UNIT_CHOICES = (
        ("cm", "CM"),
        ("ft", "FT"),
    )

    DIETARY_PREFERENCE_CHOICES = (
        ("vegan", "Vegan"),
        ("pure_vegetarian", "Pure Vegetarian"),
        ("ovo_vegetarian", "Ovo Vegetarian"),
        ("non_vegetarian", "Non Vegetarian"),
    )

    ALLERGY_CHOICES = [
        "dairy",
        "eggs",
        "fish",
        "gluten",
        "peanuts",
        "others",
        "none",
    ]

    # Used for both personal health conditions and family history
    HEALTH_CONDITION_CHOICES = [
        "diabetes_pcod_thyroid_hypertension",
        "fatty_liver_constipation_ibs",
        "arthritis_osteoporosis",
        "migraine",
        "others",
        "none",
    ]

    ACTIVITY_LEVEL_CHOICES = (
        ("not_very_active", "Not Very Active"),
        ("lightly_active", "Lightly Active"),
        ("active", "Active"),
        ("very_active", "Very Active"),
    )

    SLEEP_HOURS_CHOICES = (
        ("less_than_4", "Less than 4 hours"),
        ("4_5", "4-5 hours"),
        ("6_7", "6-7 hours"),
        ("8_10", "8-10 hours"),
    )

    YES_NO_OCCASIONALLY_CHOICES = (
        ("yes", "Yes"),
        ("no", "No"),
        ("occasionally", "Occasionally"),
    )

    YES_NO_SOCIALLY_CHOICES = (
        ("yes", "Yes"),
        ("no", "No"),
        ("socially", "Socially"),
    )

    YES_NO_CHOICES = (
        ("yes", "Yes"),
        ("no", "No"),
    )

    GOAL_CHOICES = (
        ("weight_lose", "Weight Lose"),
        ("weight_gain", "Weight Gain"),
        ("lifestyle_management", "Lifestyle Management"),
        ("stamina_mobility", "Stamina & Mobility"),
        ("strength_conditioning", "Strength & Conditioning"),
    )

    LOOKING_FOR_CHOICES = (
        ("diet_and_training", "Diet and Training Plans"),
        ("personal_training_online", "Personal Training (online, no diet plan)"),
        ("tailored_diet_plans", "Diet and Tailored Plans"),
        ("both", "Both Nutrition & Training Plans Along With An Online Trainer"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --- Step 1: Basic Info (7%) ---
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # --- Step 2: Profile Details (14%) ---
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True)
    height_unit = models.CharField(max_length=5, choices=HEIGHT_UNIT_CHOICES, blank=True)
    weight = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)

    # --- Step 3: Dietary Preference (21%) ---
    dietary_preference = models.CharField(
        max_length=20, choices=DIETARY_PREFERENCE_CHOICES, blank=True
    )

    # --- Step 4: Food Allergies (28%) ---
    food_allergies = models.JSONField(default=list, blank=True)

    # --- Step 5: Personal Health Conditions + Report Upload (35% / 42%) ---
    health_conditions = models.JSONField(default=list, blank=True)
    health_report = models.FileField(upload_to="health_reports/", null=True, blank=True)

    # --- Step 6: Family History (49%) ---
    family_health_conditions = models.JSONField(default=list, blank=True)

    # --- Step 7: Activity Level (58% / 63%) ---
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, blank=True)
    exercises_regularly = models.CharField(max_length=5, choices=YES_NO_CHOICES, blank=True)

    # --- Step 8: Lifestyle (70% / 77% / 84%) ---
    sleep_hours = models.CharField(max_length=15, choices=SLEEP_HOURS_CHOICES, blank=True)
    smokes = models.CharField(max_length=15, choices=YES_NO_OCCASIONALLY_CHOICES, blank=True)
    consumes_alcohol = models.CharField(max_length=15, choices=YES_NO_SOCIALLY_CHOICES, blank=True)

    # --- Step 9: Goals (91% / 100%) ---
    goal = models.CharField(max_length=30, choices=GOAL_CHOICES, blank=True)
    looking_for = models.CharField(max_length=30, choices=LOOKING_FOR_CHOICES, blank=True)
    target_weight = models.FloatField(null=True, blank=True)
    calorie_goal = models.PositiveIntegerField(null=True, blank=True)

    onboarding_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username