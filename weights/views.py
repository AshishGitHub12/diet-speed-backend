from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import date, timedelta

from .models import WeightLog
from .serializers import WeightLogSerializer
from profiles.models import UserProfile


def _calculate_bmi(weight, profile):
    """Mirrors the BMI formula used in profiles/serializers.py Step2Serializer."""
    if not weight or not profile or not profile.height or not profile.height_unit:
        return None
    height_m = profile.height / 100 if profile.height_unit == "cm" else profile.height * 0.3048
    if not height_m:
        return None
    return round(weight / (height_m ** 2), 2)


class AddWeightView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        entry_date = request.data.get('date') or date.today().isoformat()

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Complete onboarding before logging weight."}, status=400)

        payload = {**request.data, 'date': entry_date}

        # unique_together on (user, date) means logging again on the same day
        # updates that day's entry instead of creating a duplicate.
        try:
            instance = WeightLog.objects.get(user=user, date=entry_date)
            serializer = WeightLogSerializer(instance, data=payload, partial=True)
        except WeightLog.DoesNotExist:
            serializer = WeightLogSerializer(data=payload)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        entry = serializer.save(user=user)
        entry.bmi = _calculate_bmi(entry.weight, profile)
        entry.save()

        return Response(WeightLogSerializer(entry).data, status=201)


class WeightHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    RANGE_DAYS = {'1W': 7, '1M': 30, '3M': 90}  # 'All' (or anything else) returns everything

    def get(self, request):
        user = request.user
        range_param = request.GET.get('range', 'All')

        all_logs = WeightLog.objects.filter(user=user)  # ascending by date (model Meta.ordering)

        if range_param in self.RANGE_DAYS:
            cutoff = date.today() - timedelta(days=self.RANGE_DAYS[range_param])
            logs = all_logs.filter(date__gte=cutoff)
        else:
            logs = all_logs

        # "Current weight" should reflect the single most recent entry overall,
        # not just within whatever range is being charted.
        latest = all_logs.last()

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = None

        return Response({
            "current_weight": latest.weight if latest else None,
            "target_weight": profile.target_weight if profile else None,
            "height": profile.height if profile else None,
            "height_unit": profile.height_unit if profile else None,
            "entries": WeightLogSerializer(logs, many=True).data,
        })


class DeleteWeightView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            weight = WeightLog.objects.get(id=pk, user=request.user)
            weight.delete()
            return Response({"message": "Deleted"}, status=200)
        except WeightLog.DoesNotExist:
            return Response({"error": "Not found"}, status=404)