from django.db import models
from django.contrib.auth.models import User


def get_username(instance, filename):
	return f'{instance.user.username}/{filename}'


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to=get_username)
    type_file = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)


    