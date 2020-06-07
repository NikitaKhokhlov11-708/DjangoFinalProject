import hashlib
import os

from django.db import models


class Link(models.Model):
    original = models.URLField()
    hash = models.URLField()
    hash = models.URLField(max_length=6)
    ip = models.GenericIPAddressField()
    redir_num = models.IntegerField(default=0)

    def get_hash(self):
        gensalt = os.urandom(hashlib.blake2b.SALT_SIZE)
        key = hashlib.blake2b(salt=gensalt, digest_size=3)
        key.update(self.original.encode())
        return key.hexdigest()
