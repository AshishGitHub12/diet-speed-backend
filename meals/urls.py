from django.urls import path
from .views import (
    DietView,
    MealItemView,
    MealItemDetailView,
    FoodSearchView,
    WaterLogView,
    MealCompleteView,
)

urlpatterns = [
    path('', DietView.as_view()),                                   # GET full day summary
    path('items/', MealItemView.as_view()),                         # POST add a food entry
    path('items/<int:pk>/', MealItemDetailView.as_view()),          # DELETE an entry
    path('foods/', FoodSearchView.as_view()),                       # GET search reference DB
    path('water/', WaterLogView.as_view()),                         # POST set today's glasses
    path('meals/<str:meal_type>/complete/', MealCompleteView.as_view()),  # POST toggle completion
]