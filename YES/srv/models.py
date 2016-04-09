from django.db import models

class User(models.Model):
    name   = models.CharField(max_length=254)
    passwd = models.EmailField(max_length=254)
    email  = models.CharField(max_length=254)

    def __str__(self):
        return "{name} <{email}>".format(**dir(self))
    
class Resa(models.Model):
    user = models.ForeignKey(User)
    beg  = models.TimeField()
    end  = models.TimeField()

    def __str__(self):
        return "{beg} -> {end}".format(**dir(self))
