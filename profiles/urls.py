from django.urls import path
from .views import (
    OnboardingStep1View,
    OnboardingStep2View,
    OnboardingStep3View,
    HomeView
)

urlpatterns = [
    path("onboarding/step1/", OnboardingStep1View.as_view()),
    path("onboarding/step2/", OnboardingStep2View.as_view()),
    path("onboarding/step3/", OnboardingStep3View.as_view()),
    path("home/", HomeView.as_view(), name="home"),
]