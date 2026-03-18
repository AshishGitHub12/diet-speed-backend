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