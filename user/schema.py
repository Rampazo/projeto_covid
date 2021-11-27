from django.db import models


class UserProfileFileSchema(models.Model):

    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    user_type = models.CharField(max_length=200)
    sector = models.CharField(max_length=200)
    birthdate = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
