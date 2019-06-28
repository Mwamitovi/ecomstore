# billing/models.py
from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    data = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num = models.CharField(max_length=4)

    @property
    def display_number(self):
        return u'xxxx-xxxx-xxxx-' + str(self.num)

    def __str__(self):
        return str(self.user.username) + ' - ' + self.display_number
