from .models import WeightLog

def get_latest_weight(user):
    latest = WeightLog.objects.filter(user=user).order_by('-date').first()
    return latest.weight if latest else None