from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets
from recommender import movieservices
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .models import Rater, Rating
from .serializers import RatingSerializer

#We call this function in order to update the database before
#a response. In an evolution this should be done in the background
#with a daemon instead of calling it each time
def update_db():
    #This function will update the top rated movies for every 
    #movie service in database
    for rater in list(Rater.objects.all()):
        try:
            exec('movieservices.{}.get_top_movies()'.format(rater))
        except Exception:
            print("{} service error".format(rater))
    return True

def create_genres_list():
    genres_list=[]
    for genre in set(Rating.objects.all().values_list('genre')):
        for item in genre[0].replace(' ','').split(','):
            if item not in genres_list:
                genres_list.append(item)
    return genres_list

def create_ratings_list(ratings):
    result={}
    for item in ratings:
        if item.movie not in result.keys():
            result[item.movie]={
                'genre':item.genre,
                'rating':{
                    item.rater.name:item.rating
                }
            }
        else:
            result[item.movie]['rating'][item.rater.name]=item.rating
    return result

# User interface views
@login_required
def index(request):
    update_db()
    context={
        'user' : request.user,
        'genres_list':create_genres_list(),
        #'rating_list':set(Rating.objects.all().order_by('rating'))
        'rating_list':create_ratings_list(Rating.objects.all().order_by('-rating'))
        }
    return render(request,'recommender/index.html', context)

@login_required
def by_genre(request, genre_name):
    update_db()
    context = {
        'user' : request.user,
        'genres_list':create_genres_list(),
        'rating_list' : create_ratings_list(Rating.objects.filter(genre__icontains=genre_name).order_by('rating')),
        'genre_filter' : genre_name
        }
    return render(request, 'recommender/index.html', context)

#API Views
class RatingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RatingSerializer
    
    def get_queryset(self):
        update_db()
        queryset = Rating.objects.all() 
        """
        Optionally restricts the returned purchases to a given genre,
        by filtering against a `genre` query parameter in the URL.
        """
        genre_filter=self.request.query_params.get('genre')
        if genre_filter is not None:
            print("We are filtering by genre {}".format(genre_filter))
            queryset = queryset.filter(genre__icontains=genre_filter)
        """
        Optionally restricts the returned purchases to a given rater,
        by filtering against a `rater` query parameter in the URL.
        """
        rater_filter=self.request.query_params.get('rater')
        if rater_filter is not None:
            print("We are filtering by rater {}".format(rater_filter))
            queryset = queryset.filter(rater__name__iexact=rater_filter)
        return queryset.order_by('-rating')