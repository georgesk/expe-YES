from django.db import models
from django.contrib.auth.models import User

class Resa(models.Model):
    user = models.ForeignKey(User)
    beg  = models.TimeField()
    end  = models.TimeField()

    def __str__(self):
        return "{} -> {}".format(self.beg, self.end)
