import os
import django
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange_api.settings")
django.setup()