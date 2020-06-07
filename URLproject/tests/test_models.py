from django.test import TestCase

from URLproject import models


class LinkModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        link_db = models.Link()
        link_db.original = 'https://www.google.com/'
        link_db.hash = link_db.get_hash()
        link_db.ip = '192.168.0.1'
        link_db.save()

    def test_original_label(self):
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('original').verbose_name
        self.assertEquals(field_label, 'original')

    def test_hash_label(self):
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('hash').verbose_name
        self.assertEquals(field_label, 'hash')

    def test_redir_label(self):
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('redir_num').verbose_name
        self.assertEquals(field_label, 'redir num')

    def test_hash_max_length(self):
        link = models.Link.objects.get(id=1)
        max_length = link._meta.get_field('hash').max_length
        self.assertEquals(max_length, 6)

    def test_redir_num_default_value(self):
        link = models.Link.objects.get(id=1)
        self.assertEquals(link.redir_num, 0)
