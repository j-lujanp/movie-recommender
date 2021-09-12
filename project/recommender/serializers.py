# recommender/serializers.py
from rest_framework import serializers
from .models import Rater, Rating

class RaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rater
        fields = ('id', 'name')

class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.ReadOnlyField(source='rater.name')
    class Meta:
        model = Rating
        fields = ('id', 'movie', 'genre', 'rating', 'rater')