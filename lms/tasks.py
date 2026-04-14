from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from lms.models import Course, Subscription


@shared_task
def send_course_update_notification(course_id):
    """Отправка уведомлений подписчикам об обновлении курса"""
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)

    for subscription in subscriptions:
        user_email = subscription.user.email
        send_mail(
            subject=f'Обновление курса: {course.name}',
            message=f'Курс "{course.name}" был обновлен. Зайдите на платформу для просмотра новых материалов.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=True,
        )
    return f'Уведомления отправлены {subscriptions.count()} подписчикам'


@shared_task
def check_inactive_users():
    """Проверка неактивных пользователей (пример периодической задачи)"""
    from users.models import User
    from datetime import timedelta
    from django.utils import timezone

    threshold_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=threshold_date, is_active=True)

    # Логика для неактивных пользователей
    return f'Найдено {inactive_users.count()} неактивных пользователей'


@shared_task
def debug_task():
    """Отладочная задача"""
    print('Периодическая задача выполнена')
    return 'OK'


@shared_task
def debug_periodic_task():
    """Отладочная периодическая задача"""
    print('Периодическая задача выполнена через celery-beat')
    return 'OK'
