from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fun_fact = models.CharField(max_length = 200, default='', blank=True)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        player = Player(user=user)
        player.save()

post_save.connect(create_profile, sender=User)
