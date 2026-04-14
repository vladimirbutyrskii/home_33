from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def deactivate_inactive_users():
    """Блокировка пользователей, не заходивших более месяца"""
    month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=month_ago
    ).exclude(is_superuser=True)

    count = inactive_users.count()

    if count > 0:
        inactive_users.update(is_active=False)

    return f'Заблокировано {count} неактивных пользователей'

