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
        """ Testing the "original" field translation to human language"""
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('original').verbose_name
        self.assertEquals(field_label, 'original')

    def test_hash_label(self):
        """ Testing the "hash" field translation to human language"""
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('hash').verbose_name
        self.assertEquals(field_label, 'hash')

    def test_ip_label(self):
        """ Testing the "ip" field translation to human language"""
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('ip').verbose_name
        self.assertEquals(field_label, 'ip')

    def test_redir_label(self):
        """ Testing the "redir_num" field translation to human language"""
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('redir_num').verbose_name
        self.assertEquals(field_label, 'redir num')

    def test_hash_max_length(self):
        """ Testing the max length of the 'hash' field"""
        link = models.Link.objects.get(id=1)
        max_length = link._meta.get_field('hash').max_length
        self.assertEquals(max_length, 6)

    def test_redir_num_default_value(self):
        """ Testing the default value of the 'redir_num' field"""
        link = models.Link.objects.get(id=1)
        self.assertEquals(link.redir_num, 0)
