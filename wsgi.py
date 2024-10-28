import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTING_MODULE', 'Rule_Engine.settings')

application = get_wsgi_application()

app = application