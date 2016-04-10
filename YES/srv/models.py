from django.db import models
from django.contrib.auth.models import User

class Resa(models.Model):
    user = models.ForeignKey(User)
    beg  = models.DateTimeField()
    end  = models.DateTimeField()

    def __str__(self):
        return "{} -> {} ({})".format(self.beg, self.end, self.user.username)
