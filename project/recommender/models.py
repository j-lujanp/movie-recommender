from django.db import models

#This class stores the information of the platforms that rate the movies
class Rater(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Rating(models.Model):
	movie = models.CharField(max_length=100)
	#We are storing genre as a string instead of a separated model because each
	#movie service will add all the genres a movie belongs to
	#In an evolution, this should be changed and the movie service
	#would separate the fields before storing data
	genre = models.CharField(max_length=100)
	rating = models.IntegerField(default=0)
	rater = models.ForeignKey(Rater, on_delete=models.CASCADE)
	def __str__(self):
		return "{} (rating {} from {})".format(self.movie, self.rating, self.rater.name)


#This model is only use to test a differente movie service
class LocalDBService(models.Model):
	movie = models.CharField(max_length=100)
	genre = models.CharField(max_length=100)
	rating = models.IntegerField(default=0)
	def __str__(self):
		return "{} ({})".format(self.movie, self.rating)