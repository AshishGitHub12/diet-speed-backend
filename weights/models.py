from django.db import models
from django.contrib.auth.models import User

class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    weight = models.FloatField()
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['date']

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg on {self.date}"