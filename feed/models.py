from cgitb import text

from django.db import models
from django.contrib.auth. models import User

# Create your models here.
app_name = 'feed'

class Post(models.Model):

    text= models.CharField(max_length=200,null=False)
    date= models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):

        return self.text

