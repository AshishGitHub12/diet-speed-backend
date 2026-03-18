from django.urls import path
from .views import AddWeightView, WeightHistoryView, DeleteWeightView

urlpatterns = [
    path('', AddWeightView.as_view()),
    path('history/', WeightHistoryView.as_view()),
    path('<int:pk>/', DeleteWeightView.as_view()),
]