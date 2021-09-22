from django.db import models

# Create your models here.
class ChatUsers(models.Model):
    User = models.CharField(max_length=100)
    FatCalls = models.IntegerField(default=0)
    StupidCalls = models.IntegerField(default=0)
    DumbCalls = models.IntegerField(default=0)
