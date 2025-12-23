from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User, Team, Activity, Workout, Leaderboard

class APISmokeTest(APITestCase):
	def test_api_root(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn('users', response.data)

	def test_users_list(self):
		response = self.client.get('/users/')
		self.assertEqual(response.status_code, 200)

	def test_teams_list(self):
		response = self.client.get('/teams/')
		self.assertEqual(response.status_code, 200)

	def test_activities_list(self):
		response = self.client.get('/activities/')
		self.assertEqual(response.status_code, 200)

	def test_workouts_list(self):
		response = self.client.get('/workouts/')
		self.assertEqual(response.status_code, 200)

	def test_leaderboards_list(self):
		response = self.client.get('/leaderboards/')
		self.assertEqual(response.status_code, 200)
