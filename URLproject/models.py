import binascii
import hashlib
import os

from django.db import models


class Link(models.Model):
    original = models.URLField()
    hash = models.CharField(max_length=9)
    redir_num = models.IntegerField(default=0)

    def get_hash(self):
        salt = os.urandom(10)
        key = hashlib.pbkdf2_hmac('sha256', self.original.encode(), salt, 100000)

        return binascii.hexlify(key).decode()[:6]
