from django.test import TestCase
from django.urls import reverse
from .models import Game


class TicTacGameViewTests(TestCase):
    def test_room_creation_persists_game_and_redirects_to_play(self):
        response = self.client.post(
            reverse('home'),
            {'username': 'Alice', 'option': '2', 'room_code': 'A1B2C3'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Game.objects.filter(room_code='A1B2C3', game_creator='Alice').exists())

    def test_play_page_renders_with_room_and_username_context(self):
        Game.objects.create(room_code='A1B2C3', game_creator='Alice', game_opponent='Bob')
        response = self.client.get('/play/A1B2C3/?username=Alice', {'username': 'Alice'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'room_code')
