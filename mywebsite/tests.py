from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestHomePageHTML(TestCase):

    def test_home_page_is_displayed(self):
        user1 = User.objects.create(username='Tom', password='12345678')
        user2 = User.objects.create(username='Jerry', password='12345678')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(len(response.context['users']), 2)
        self.assertContains(response, 'Tom')
        self.assertContains(response, 'Jerry')

    def test_no_users(self):
        User.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['users']), 0)
        self.assertContains(response, 'No users')
