from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
import uuid
from django.dispatch import receiver

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DCI = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    def __unicode__(self):
        return u'{}, {}'.format(self.user.last_name, self.user.first_name)

#def create_profile(sender, **kwargs):
#    user = kwargs["instance"]
#    if kwargs["created"]:
#        player = Player(user=user)
#        player.save()

#post_save.connect(create_profile, sender=User)
@receiver(post_save, sender=User)
def create_player_for_new_user(sender, created, instance, **kwargs):
    if created:
        player = Player(user=instance)
        player.save()

class Tournament(models.Model):
    host = models.ForeignKey(Player)
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000) #description
    def __unicode__(self):
        return u'{}\'s {}'.format(self.host.user.username, self.name)

class Match(models.Model):
    player1 = models.ForeignKey(Player, related_name='winner') #sender of match results 
    player2 = models.ForeignKey(Player, related_name='loser') #verifier of match results
    wins = models.PositiveIntegerField(default=0) #number of player1 wins
    loss = models.PositiveIntegerField(default=0) #number of player1 loss
    ties = models.PositiveIntegerField(default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)
    tournament = models.ForeignKey(Tournament)

STATUS_CHOICES = (
    ('1', 'Unverified'),
    ('2', 'Confirm'),
    ('3', 'Decline'),
)

class ScoreRequest(models.Model):
    player1 = models.ForeignKey(Player, related_name='requester') #sender of match results 
    player2 = models.ForeignKey(Player, related_name='confirmer') #verifier of match results
    wins = models.PositiveIntegerField(default=0) #number of player1 wins
    loss = models.PositiveIntegerField(default=0) #number of player1 loss
    ties = models.PositiveIntegerField(default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)
    tournament = models.ForeignKey(Tournament)
    verified = models.IntegerField(choices=STATUS_CHOICES, default=1)
