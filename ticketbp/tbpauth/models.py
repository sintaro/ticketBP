from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    address1 = models.CharField("住所1", max_length=32, blank=True, null=True)
    address2 = models.CharField("住所2", max_length=128, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        db_table = 'user'
        swappable = 'AUTH_USER_MODEL'

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name

    def address(self):
        return self.address1 + ' ' + self.address2
