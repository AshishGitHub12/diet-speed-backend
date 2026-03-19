from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from datetime import date
from .serializers import Step1Serializer, Step2Serializer, Step3Serializer, ProfileSerializer
from weights.utils import get_latest_weight


class OnboardingStep1View(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            profile = UserProfile.objects.get(user=request.user)

            serializer = Step1Serializer(
                profile,
                data=request.data,
                partial=True
            )

        except UserProfile.DoesNotExist:

            serializer = Step1Serializer(data=request.data)

        if serializer.is_valid():

            profile = serializer.save(user=request.user)

            return Response({
                "message": "Step 1 saved"
            })

        return Response(serializer.errors, status=400)

class OnboardingStep2View(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = Step2Serializer(data=request.data)

        if serializer.is_valid():

            height = serializer.validated_data["height"]
            unit = serializer.validated_data["height_unit"]
            weight = serializer.validated_data["weight"]

            bmi = serializer.calculate_bmi(height, unit, weight)

            profile = UserProfile.objects.get(user=request.user)

            profile.height = height
            profile.height_unit = unit
            profile.weight = weight
            profile.bmi = bmi

            profile.save()

            return Response({"bmi": bmi})

        return Response(serializer.errors)

class OnboardingStep3View(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        profile = UserProfile.objects.get(user=request.user)

        serializer = Step3Serializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            profile = serializer.save()

            # ✅ mark onboarding completed
            profile.onboarding_completed = True
            profile.save()

            return Response({
                "message": "Onboarding completed"
            })

        return Response(serializer.errors, status=400)


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get user profile
        profile = UserProfile.objects.get(user=user)

        # BMI category logic
        bmi = profile.bmi
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25:
            bmi_category = "Normal"
        else:
            bmi_category = "Overweight"

        # User data
        user_data = {
            "name": profile.name,
            "current_weight": profile.weight,
            "target_weight": profile.target_weight,
            "bmi": profile.bmi,
            "bmi_category": bmi_category,
        }

        # Date data
        today = date.today()
        date_data = {
            "today_date": today,
            "day_name": today.strftime("%A"),
        }

        # Static Success Stories
        success_stories = [
            {
                "id": 1,
                "name": "Rahul",
                "result": "Lost 10kg",
                "image": "https://example.com/image1.jpg"
            },
            {
                "id": 2,
                "name": "Neha",
                "result": "Lost 8kg",
                "image": "https://example.com/image2.jpg"
            }
        ]

        # Static Recipes
        recipes = [
            {
                "id": 1,
                "name": "Salad",
                "image": "https://example.com/salad.jpg",
                "calories": 200
            },
            {
                "id": 2,
                "name": "Oats",
                "image": "https://example.com/oats.jpg",
                "calories": 150
            }
        ]

        # Static Workouts
        workouts = [
            {
                "id": 1,
                "title": "Full Body Workout",
                "thumbnail": "https://example.com/workout.jpg",
                "video_url": "https://youtube.com/example",
                "duration": "20 min"
            }
        ]

        # Final Response
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
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        serializer = ProfileSerializer(profile)
        data = serializer.data

        # ✅ Override weight with latest weight
        latest_weight = get_latest_weight(request.user)
        if latest_weight:
            data["weight"] = latest_weight

        return Response(data)