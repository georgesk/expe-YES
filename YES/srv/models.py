from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import pytz

class Resa(models.Model):
    user = models.ForeignKey(User)
    beg  = models.DateTimeField()
    end  = models.DateTimeField()

    def __str__(self):
        return "{} -> {} ({})".format(self.beg, self.end, self.user.username)

class Profile(models.Model):
    """
    add a few additional data for a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=7, choices=settings.LANGUAGES)
    timezone = models.CharField(max_length=25, choices=[(tz,tz) for tz in pytz.common_timezones])

    def __str__(self):
        return "{} ({},{})".format(self.user, self.language, self.timezone)
