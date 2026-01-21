from django.test import TestCase, Client
from django.urls import reverse

class DemoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('demo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/index.html')

    def test_styleguide_view(self):
        response = self.client.get(reverse('demo:styleguide'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/styleguide.html')

    def test_movies_view(self):
        response = self.client.get(reverse('demo:movies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/movies.html')

    def test_actors_view(self):
        response = self.client.get(reverse('demo:actors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/actors.html')

    def test_music_view(self):
        response = self.client.get(reverse('demo:music'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'demo/music.html')
