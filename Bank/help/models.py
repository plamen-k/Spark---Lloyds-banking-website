# Code written by Plamen Kolev

from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class StaticQuestion(models.Model):
    question = models.CharField(max_length=120)
    answer = HTMLField()
    dateCreated = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())

    def __str__(self):
        return self.question

class FormQuestion(models.Model):
    question = models.TextField(max_length=1020)
    name = models.CharField(max_length=300)
    email = models.EmailField()
    dateCreated = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())
    answered = models.BooleanField(default=False)

