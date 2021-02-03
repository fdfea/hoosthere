from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=50, blank=True)
    minor = models.CharField(max_length=50, blank=True)
    classes_taken = models.CharField(max_length=500, blank=True)
    private = models.BooleanField(default=False)
    #add more fields as necessary

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, related_name='viewer', on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    read = models.BooleanField(default=False)

class MessageSummary(Message): #proxy model...does not effect the database
    class Meta:
        proxy=True
        verbose_name = 'Message Summary'
        verbose_name_plural = 'Messages Summary'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class MessageBoardCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Message Board Category"
        verbose_name_plural = "Message Board Categories"

    def __str__(self):
        return self.name

class MessageBoardPost(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(MessageBoardCategory, on_delete=models.CASCADE)
    message_title = models.CharField(max_length=200)
    message_body = models.TextField() #max_length is set to None
    date_posted = models.DateTimeField(default=datetime.now, editable=True)

    class Meta:
        verbose_name = "Message Board Post"
        verbose_name_plural = "Message Board Posts"

    def __str__(self):
        return self.message_title
