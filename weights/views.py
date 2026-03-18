from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date

from .models import WeightLog
from .serializers import WeightLogSerializer
from profiles.models import UserProfile


class AddWeightView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        weight = request.data.get('weight')
        entry_date = request.data.get('date', date.today())

        try:
            weight_obj = WeightLog.objects.get(user=user, date=entry_date)
            weight_obj.weight = weight
            weight_obj.save()
            return Response({"message": "Weight updated"}, status=200)
        except WeightLog.DoesNotExist:
            WeightLog.objects.create(user=user, weight=weight, date=entry_date)
            return Response({"message": "Weight added"}, status=201)

class WeightHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        range_param = request.GET.get('range', 'all')

        logs = WeightLog.objects.filter(user=user)

        if range_param != 'all':
            days = int(range_param)
            from datetime import timedelta
            logs = logs.filter(date__gte=date.today() - timedelta(days=days))

        data = [
            {"date": log.date, "weight": log.weight}
            for log in logs
        ]

        latest = logs.last()

        profile = UserProfile.objects.get(user=user)

        return Response({
            "current_weight": latest.weight if latest else None,
            "target_weight": profile.target_weight,
            "data": data
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