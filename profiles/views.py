from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .serializers import Step1Serializer, Step2Serializer, Step3Serializer


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