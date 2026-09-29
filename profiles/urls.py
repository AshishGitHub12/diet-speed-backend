from django.urls import path
from .views import (
    OnboardingStep1View,
    OnboardingStep2View,
    OnboardingStep3View,
    OnboardingStep4View,
    OnboardingStep5View,
    OnboardingStep6View,
    OnboardingStep7View,
    OnboardingStep8View,
    OnboardingStep9View,
    HomeView,
    ProfileView,
)

urlpatterns = [
    path("onboarding/step1/", OnboardingStep1View.as_view()),  # Basic Info: name, email, phone
    path("onboarding/step2/", OnboardingStep2View.as_view()),  # Profile Details: dob, gender, height, weight
    path("onboarding/step3/", OnboardingStep3View.as_view()),  # Dietary preference
    path("onboarding/step4/", OnboardingStep4View.as_view()),  # Food allergies
    path("onboarding/step5/", OnboardingStep5View.as_view()),  # Health conditions + report upload
    path("onboarding/step6/", OnboardingStep6View.as_view()),  # Family history
    path("onboarding/step7/", OnboardingStep7View.as_view()),  # Activity level + exercise
    path("onboarding/step8/", OnboardingStep8View.as_view()),  # Lifestyle: sleep, smoking, alcohol
    path("onboarding/step9/", OnboardingStep9View.as_view()),  # Goal + looking-for (final step)
    path("home/", HomeView.as_view(), name="home"),
    path("profile/", ProfileView.as_view()),
]