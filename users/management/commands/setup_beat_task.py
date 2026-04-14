from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = 'Создание периодической задачи через celery-beat'

    def handle(self, *args, **options):
        # Создаем интервал (каждые 60 секунд)
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=60,
            period=IntervalSchedule.SECONDS,
        )

        # Создаем периодическую задачу
        PeriodicTask.objects.get_or_create(
            name='Debug task every 60 seconds',
            defaults={
                'task': 'lms.tasks.debug_periodic_task',
                'interval': schedule,
                'enabled': True,
            }
        )

        self.stdout.write(self.style.SUCCESS('Периодическая задача создана'))

