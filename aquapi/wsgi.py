"""
WSGI config for AquaPi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

# http://stackoverflow.com/a/14876533
import os, sys
sys.path.append(' /opt/AquaPi/aquapi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AquaPi.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
