import os
import sys
sys.path.append('/home/ubuntu/project1/project1')
os.environ.setdefault("PYTHON_EGG_CACHE", "/home/ubuntu/project1/project1/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project1.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()