from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

#For the API REST
router = DefaultRouter()
router.register(r'ratings', views.RatingViewSet, basename='rating')


app_name='recommender'
urlpatterns = [
        path('', views.index, name="index"),
        path('genre/<str:genre_name>/', views.by_genre, name="by_genre"),
        #API REST views
        path("api/", include(router.urls))
        ]
