from django.db import models

class User(models.Model):
  username = models.CharField(max_length=255,null=True)
  password = models.CharField(max_length=255,null=True)

  def __str__(self):
    return f"{self.username} {self.password}"