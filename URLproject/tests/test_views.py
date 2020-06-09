from django.test import TestCase, Client
from django.urls import reverse

from URLproject import models
from URLproject.models import Link


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        link_db = models.Link()
        link_db.original = 'https://www.google.com/'
        link_db.hash = link_db.get_hash()
        link_db.ip = '192.168.0.1'
        link_db.save()
        link_db = models.Link()
        link_db.original = 'https://www.google.com/'
        link_db.hash = link_db.get_hash()
        link_db.ip = '192.168.1.0'
        link_db.save()

    def test_call_view_index_get(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertNotContains(response, 'Сокращенная ссылка:')

    def test_call_view_index_post_empty_link(self):
        url = reverse('index')
        response = self.client.post(url, {'url': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Неверный формат ссылки!')

    def test_call_view_index_post_wrong_link(self):
        url = reverse('index')
        response = self.client.post(url, {'url': 'https://sdfsdfsdf   www.google.com/'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Неверный формат ссылки!')

    def test_call_view_index_post_normal_link(self):
        url = reverse('index')
        response = self.client.post(url, {'url': 'https://www.google.com/'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Сокращенная ссылка:')

    def test_call_view_all_get(self):
        url = reverse('all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'links.html')
        all_links = response.context['all_results']
        self.assertCountEqual(all_links, Link.objects.all())

    def test_call_view_mine_get(self):
        self.client = Client(REMOTE_ADDR='192.168.0.1')
        url = reverse('mine')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'links.html')
        my_links = response.context['mine_results']
        self.assertCountEqual(my_links, Link.objects.all().filter(ip='192.168.0.1'))

    def test_call_view_mine_empty(self):
        self.client = Client(REMOTE_ADDR='192.168.1.1')
        url = reverse('mine')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'links.html')
        my_links = response.context['mine_results']
        self.assertCountEqual(my_links, Link.objects.all().filter(ip='192.168.1.1'))

    def test_call_view_delete_error(self):
        self.client = Client(REMOTE_ADDR='192.168.1.1')
        url = reverse('delete', kwargs={'linkid': 1})
        response = self.client.get(url, {'id': 1})
        self.assertRedirects(response, '/mine/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertEquals(Link.objects.all().count(), 2)

    def test_call_view_deleted(self):
        self.client = Client(REMOTE_ADDR='192.168.0.1')
        url = reverse('delete', kwargs={'linkid': 1})
        response = self.client.get(url, {'id': 1})
        self.assertRedirects(response, '/mine/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertEquals(Link.objects.all().count(), 1)

    def test_call_view_redirect_error(self):
        url = reverse('redir', args=['sdsfa'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_call_view_redirect_true(self):
        url = reverse('redir', args=[Link.objects.all()[1].hash])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Link.objects.all()[1].redir_num, 1)
