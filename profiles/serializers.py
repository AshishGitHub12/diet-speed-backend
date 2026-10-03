from rest_framework import serializers
from .models import UserProfile


def _validate_choices(value, allowed, field_label):
    for item in value:
        if item not in allowed:
            raise serializers.ValidationError(f"{item} is not a valid {field_label} option")
    return value


class Step1Serializer(serializers.ModelSerializer):
    """Basic Info screen — name, email, phone number (7%)"""

    class Meta:
        model = UserProfile
        fields = ["name", "email", "phone_number"]


class Step2Serializer(serializers.ModelSerializer):
    """Profile Details screen — dob, gender, height, weight (14%). Recalculates BMI."""

    class Meta:
        model = UserProfile
        fields = ["dob", "gender", "height", "height_unit", "weight"]

    def calculate_bmi(self, height, unit, weight):
        height_m = height / 100 if unit == "cm" else height * 0.3048
        return round(weight / (height_m ** 2), 2)

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        if instance.height and instance.weight and instance.height_unit:
            instance.bmi = self.calculate_bmi(instance.height, instance.height_unit, instance.weight)
            instance.save()
        return instance


class Step3Serializer(serializers.ModelSerializer):
    """Dietary preference screen (21%)"""

    class Meta:
        model = UserProfile
        fields = ["dietary_preference"]


class Step4Serializer(serializers.ModelSerializer):
    """Food allergies screen (28%)"""

    food_allergies = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = UserProfile
        fields = ["food_allergies"]

    def validate_food_allergies(self, value):
        return _validate_choices(value, UserProfile.ALLERGY_CHOICES, "allergy")


class Step5Serializer(serializers.ModelSerializer):
    """Personal health conditions + optional report upload (35% / 42%)"""

    health_conditions = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = UserProfile
        fields = ["health_conditions", "health_report"]

    def validate_health_conditions(self, value):
        return _validate_choices(value, UserProfile.HEALTH_CONDITION_CHOICES, "health condition")


class Step6Serializer(serializers.ModelSerializer):
    """Family history of health conditions screen (49%)"""

    family_health_conditions = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = UserProfile
        fields = ["family_health_conditions"]

    def validate_family_health_conditions(self, value):
        return _validate_choices(value, UserProfile.HEALTH_CONDITION_CHOICES, "health condition")


class Step7Serializer(serializers.ModelSerializer):
    """Activity level + whether they exercise regularly (58% / 63%)"""

    class Meta:
        model = UserProfile
        fields = ["activity_level", "exercises_regularly"]


class Step8Serializer(serializers.ModelSerializer):
    """Lifestyle screen — sleep, smoking, alcohol (70% / 77% / 84%)"""

    class Meta:
        model = UserProfile
        fields = ["sleep_hours", "smokes", "consumes_alcohol"]


class Step9Serializer(serializers.ModelSerializer):
    """Final step — goal, plan preference, optional target weight (91% / 100%)"""

    class Meta:
        model = UserProfile
        fields = ["goal", "looking_for", "target_weight"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ["user", "bmi", "onboarding_completed"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        height = validated_data.get("height", instance.height)
        weight = validated_data.get("weight", instance.weight)
        height_unit = validated_data.get("height_unit", instance.height_unit)

        if height and weight:
            height_m = (height * 30.48 if height_unit == "ft" else height) / 100
            instance.bmi = round(weight / (height_m ** 2), 2)

        instance.save()
        return instance