from django.test import TestCase, Client
from django.urls import reverse

from recommender import views
from .models import Rater
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User

def login():
	client=Client()
	user=User.objects.create_user('foo', password='bar')
	user.save()
	client.login(username="foo", password="bar")
	return client

#Tests for views
class IndexViewTest(TestCase):

	def test_index_access(self):
		client=Client()
		response = client.get(reverse('recommender:index'))
		self.assertEqual(response.status_code, 302)
		client=login()
		response = client.get(reverse('recommender:index'))
		self.assertEqual(response.status_code, 200)

	
	def test_no_ratings(self):
		client=login()
		"""
    	If no ratings exist, an appropriate message is displayed.
    	"""
		response = client.get(reverse('recommender:index'))
		self.assertContains(response, "No suggestions available.")

#Test for services and other functions

class MovieServicesTest(TestCase):
	def test_update_db(self):
		"""
		This test checks that the database is updated even
		if some implementations are not done
		"""
		rater=Rater.objects.create(name="TestService")
		rater.save()
		rater=Rater.objects.create(name="Netflix")
		rater.save()
		result=views.update_db()
		self.assertEqual(result,True)

#Test for the API

class RaterAPITest(TestCase):
	def test_rater_api_get_access(self):
		client=Client()
		response = client.get('/recommender/api/raters/')
		self.assertEqual(response.status_code, 403)
		client=login()
		response = client.get('/recommender/api/raters/')
		self.assertEqual(response.status_code, 200)

	def test_rater_api_create_update_and_delete(self):
		client=login()
		response = client.post(
			'/recommender/api/raters/',
			{
				'name':'testrater'
			},
			format='json')
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data, {'id':1,'name':'testrater'})
		response = client.patch(
			'/recommender/api/raters/1/',
			{
				'name':'testrater2'
			},
			content_type='application/json',
			format='json')
		self.assertEqual(response.status_code, 200)
		response = client.get('/recommender/api/raters/1/')
		self.assertEqual(response.data, {'id':1,'name':'testrater2'})
		response = client.delete('/recommender/api/raters/1/')
		self.assertEqual(response.status_code, 204)
