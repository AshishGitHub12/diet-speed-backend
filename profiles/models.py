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

    MEDICAL_CONDITION_CHOICES = [
        "diabetes",
        "thyroid",
        "pcos",
        "hypertension",
        "heart_disease",
        "asthma",
        "none"
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    height = models.FloatField()
    height_unit = models.CharField(max_length=5, choices=HEIGHT_UNIT_CHOICES)
    weight = models.FloatField()

    bmi = models.FloatField(null=True, blank=True)

    target_weight = models.FloatField(null=True, blank=True)

    # Store selected conditions
    medical_conditions = models.JSONField(default=list, blank=True)

    onboarding_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username