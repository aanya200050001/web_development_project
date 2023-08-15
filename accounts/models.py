from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import requests


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField(null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    username = instance.username
    Repository.objects.all().delete()
    repo_response = requests.get('https://api.github.com/users/' + username + '/repos').json()
    if type(repo_response) is list:
        for repo in repo_response:
            repository =  Repository(name = repo["name"], no_of_stars = repo["stargazers_count"], profile = instance.profile)
            repository.save()
        user_response = requests.get('https://api.github.com/users/' + username).json()
        instance.profile.followers = user_response["followers"]
        instance.profile.updated_at = user_response["updated_at"]
    instance.profile.save()

class Repository(models.Model):
    name = models.CharField(max_length=50)
    no_of_stars = models.IntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)