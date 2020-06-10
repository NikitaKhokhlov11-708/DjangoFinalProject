import hashlib
import os

from django.db import models


class Link(models.Model):
    """Model of the Link object"""
    original = models.URLField()  # Original link
    hash = models.CharField(max_length=6)  # 6 chars hash code of the link
    ip = models.GenericIPAddressField()  # IP address of the user
    redir_num = models.IntegerField(default=0)  # Number of redirects using short link

    def get_hash(self):
        """ Hash generation method

        :return: 6 chars hashcode of original link
        """
        gensalt = os.urandom(hashlib.blake2b.SALT_SIZE)  # Generated salt
        key = hashlib.blake2b(salt=gensalt, digest_size=3)
        key.update(self.original.encode())  # Generated hash
        return key.hexdigest()
