from abc import ABC, abstractmethod
import json
from .models import Rating, LocalDBService, Rater
from django.core import serializers

#This function updates or creates the new records received by the movie services
#Receives a list of dicts
def update_ratings(updated_ratings, myrater):
	for item in updated_ratings:

		obj, created = Rating.objects.update_or_create(
			rater=myrater, movie=item['movie'],
			defaults={
				'genre': item['genre'],
				'rating': item['rating']}
			)
	return True

#This class represent all the functions that the movie services need to implement
class MovieService(ABC):
	@abstractmethod
	def get_top_movies(self):
		#This method call the API of the movie service
		#and fetch the top movies
		#We can filter by genre using the parameter
		#The method must return a list of dicts in JSON format
		#including the fields: genre, movie and rating
		pass

class Netflix(MovieService):
	#This service reads a local file with movie information in JSON format
	def get_top_movies():
		myrater=Rater.objects.all().filter(name="Netflix")[0]
		#print("Top movies from Netflix")
		with open('recommender/test_data/netflix.json', 'r') as myfile:
			data = myfile.read()
		data=json.loads(data)
		update_ratings(data, myrater) 

class LocalDB(MovieService):
	#This service reads information from a local database
	def get_top_movies():
		myrater=Rater.objects.all().filter(name="LocalDB")[0]
		localDBratings=list(LocalDBService.objects.all().values())
		update_ratings(localDBratings,myrater)