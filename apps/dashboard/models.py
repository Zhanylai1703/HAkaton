from django.db import models

from apps.users.models import User, Department

from django.utils import timezone


class Report(models.Model):
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='report_user'
    )
    department = models.ForeignKey(
        'users.Department', 
        on_delete=models.CASCADE, 
        related_name='dep_report'
    )
    week_start_date = models.DateField()
    last_week = models.TextField(
        null=True, blank=True, 
        verbose_name='отчет за прошлую неделю'
    )
    current_week = models.TextField(
        null=True, blank=True, 
        verbose_name='отчет за эту неделю'
    )
    next_week = models.TextField(
        null=True, blank=True, 
        verbose_name='отчет на следующую неделю'
    )
    deadline = models.DateField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    sent = models.BooleanField(
        default=False, 
        verbose_name='Отчет отправлен'
    )
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.week_start_date = timezone.now().date()
            self.deadline = self.week_start_date + timezone.timedelta(days=7)
        super(Report, self).save(*args, **kwargs)

    def __str__(self):
        return f"Report {self.id} by {self.user.username}"


