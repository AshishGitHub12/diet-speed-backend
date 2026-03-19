from rest_framework import serializers
from .models import UserProfile


class Step1Serializer(serializers.ModelSerializer):

    medical_conditions = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            "name",
            "dob",
            "gender",
            "height",
            "height_unit",
            "weight",
            "medical_conditions",
        ]

    def validate_medical_conditions(self, value):

        allowed = UserProfile.MEDICAL_CONDITION_CHOICES

        for condition in value:
            if condition not in allowed:
                raise serializers.ValidationError(
                    f"{condition} is not a valid medical condition"
                )

        return value

class Step2Serializer(serializers.Serializer):

    height = serializers.FloatField()
    height_unit = serializers.CharField()
    weight = serializers.FloatField()

    def calculate_bmi(self, height, unit, weight):

        if unit == "cm":
            height_m = height / 100

        elif unit == "ft":
            height_m = height * 0.3048

        else:
            raise serializers.ValidationError("Invalid height unit")

        bmi = weight / (height_m ** 2)

        return round(bmi, 2)

class Step3Serializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["target_weight"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ["user", "bmi", "onboarding_completed"]

    def update(self, instance, validated_data):
        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Recalculate BMI if height or weight changes
        height = validated_data.get("height", instance.height)
        weight = validated_data.get("weight", instance.weight)
        height_unit = validated_data.get("height_unit", instance.height_unit)

        if height and weight:
            if height_unit == "ft":
                height = height * 30.48  # ft → cm

            height_m = height / 100
            instance.bmi = round(weight / (height_m ** 2), 2)

        instance.save()
        return instance