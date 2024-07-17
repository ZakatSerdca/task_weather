from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CitySearch
import json
from unittest.mock import patch

class WeatherViewsTestCase(TestCase):
    """
    Тесты для представлений weather/views.py
    """

    def setUp(self):
        """
        Создает пользователя и логинится
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_home_view_get(self):
        """
        Тест для GET запроса на главную страницу
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/home.html')

    @patch('weather.views.get_weather_data')
    def test_home_view_post(self, mock_get_weather_data):
        """
        Тест для POST запроса на главную страницу
        """
        mock_get_weather_data.return_value = {
            'city': 'Test City',
            'latitude': 0.0,
            'longitude': 0.0,
            'temperature': 25,
            'weather': 1
        }
        response = self.client.post(reverse('home'), {'city': 'Test City'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/home.html')
        self.assertContains(response, 'Weather in Test City')
        self.assertTrue(CitySearch.objects.filter(user=self.user, city='Test City').exists())

    def test_city_autocomplete(self):
        """
        Тест для функции автокомплита
        """
        with patch('weather.views.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'results': [{'name': 'Test City'}, {'name': 'Test City 2'}]
            }
            response = self.client.get(reverse('city_autocomplete'), {'query': 'Test'})
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['suggestions'], ['Test City', 'Test City 2'])

