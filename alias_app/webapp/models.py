from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from .conf import settings


@python_2_unicode_compatible
class Settings(models.Model):
    user = models.OneToOneField(User)
    is_setup_done = models.BooleanField(default=False)
    hosting_service = models.ForeignKey('HostingService', blank=True, null=True)
    api_key = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "Settings for {}".format(self.user.username)


@python_2_unicode_compatible
class HostingService(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    handler = models.CharField(_("Handler"), max_length=50, choices=settings.HOSTING_SERVICES_HANDLERS)

    def __str__(self):
        return self.name

    def get_handler(self):
        module_name = ".".join([settings.HANDLERS_PATH, self.handler])
        return __import__(module_name, globals(), locals(), [str('Handler'), ], -1)
