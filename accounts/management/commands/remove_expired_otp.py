from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = 'Remove expired codes'

    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('Expired otp codes removed.')
