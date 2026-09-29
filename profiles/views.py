from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import UserProfile
from datetime import date
from .serializers import (
    Step1Serializer,
    Step2Serializer,
    Step3Serializer,
    Step4Serializer,
    Step5Serializer,
    Step6Serializer,
    Step7Serializer,
    Step8Serializer,
    Step9Serializer,
    ProfileSerializer,
)
from weights.utils import get_latest_weight


class BaseOnboardingStepView(APIView):
    """
    Shared logic for every onboarding step:
    get-or-create the profile for the logged-in user, then save a
    partial update using whichever serializer the subclass declares.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = None
    mark_completed = False

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={"name": request.user.get_full_name() or request.user.username},
        )

        serializer = self.serializer_class(profile, data=request.data, partial=True)

        if serializer.is_valid():
            profile = serializer.save()

            if self.mark_completed:
                profile.onboarding_completed = True
                profile.save()

            return Response({
                "message": "Saved",
                "onboarding_completed": profile.onboarding_completed,
                "data": ProfileSerializer(profile).data,
            })

        return Response(serializer.errors, status=400)


class OnboardingStep1View(BaseOnboardingStepView):
    """Basic Info — name, email, phone (7%)"""
    serializer_class = Step1Serializer


class OnboardingStep2View(BaseOnboardingStepView):
    """Profile Details — dob, gender, height, weight (14%)"""
    serializer_class = Step2Serializer


class OnboardingStep3View(BaseOnboardingStepView):
    """Dietary preference (21%)"""
    serializer_class = Step3Serializer


class OnboardingStep4View(BaseOnboardingStepView):
    """Food allergies (28%)"""
    serializer_class = Step4Serializer


class OnboardingStep5View(BaseOnboardingStepView):
    """Health conditions + report upload (35% / 42%)"""
    serializer_class = Step5Serializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class OnboardingStep6View(BaseOnboardingStepView):
    """Family history of health conditions (49%)"""
    serializer_class = Step6Serializer


class OnboardingStep7View(BaseOnboardingStepView):
    """Activity level + exercise (58% / 63%)"""
    serializer_class = Step7Serializer


class OnboardingStep8View(BaseOnboardingStepView):
    """Lifestyle — sleep, smoking, alcohol (70% / 77% / 84%)"""
    serializer_class = Step8Serializer


class OnboardingStep9View(BaseOnboardingStepView):
    """Goal + looking-for plan type. Final step, marks onboarding complete (91% / 100%)"""
    serializer_class = Step9Serializer
    mark_completed = True


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        profile = UserProfile.objects.get(user=user)

        latest_weight = get_latest_weight(user)

        height = profile.height
        unit = profile.height_unit

        bmi = None

        if latest_weight and height and unit:
            height_m = height / 100 if unit == "cm" else height
            bmi = round(latest_weight / (height_m ** 2), 2)

        if bmi is None:
            bmi_category = "Not Available"
        elif bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25:
            bmi_category = "Normal"
        else:
            bmi_category = "Overweight"

        user_data = {
            "name": profile.name,
            "current_weight": latest_weight,
            "target_weight": profile.target_weight,
            "bmi": bmi,
            "bmi_category": bmi_category,
        }

        today = date.today()
        date_data = {
            "today_date": today,
            "day_name": today.strftime("%A"),
        }

        success_stories = [
            {"id": 1, "name": "Rahul", "result": "Lost 10kg", "image": "https://example.com/image1.jpg"},
            {"id": 2, "name": "Neha", "result": "Lost 8kg", "image": "https://example.com/image2.jpg"},
        ]

        recipes = [
            {"id": 1, "name": "Salad", "image": "https://example.com/salad.jpg", "calories": 200},
            {"id": 2, "name": "Oats", "image": "https://example.com/oats.jpg", "calories": 150},
        ]

        workouts = [
            {
                "id": 1,
                "title": "Full Body Workout",
                "thumbnail": "https://example.com/workout.jpg",
                "video_url": "https://youtube.com/example",
                "duration": "20 min",
            }
        ]

        data = {
            "user": user_data,
            "date": date_data,
            "success_stories": success_stories,
            "recipes": recipes,
            "workouts": workouts,
        }

        return Response(data)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=404)

        serializer = ProfileSerializer(profile)
        data = serializer.data

        latest_weight = get_latest_weight(request.user)
        if latest_weight:
            data["weight"] = latest_weight

        return Response(data)