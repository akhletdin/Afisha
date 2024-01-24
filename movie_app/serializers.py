from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ('id', 'name', 'movie_count')

    def get_movie_count(self, director):
        return [movie.title for movie in director.movies.all()]


class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director_name average_rating reviews'.split()
        # exclude = 'id'.split()
        depth = 1

    def get_average_rating(self, review):
        return review.rating


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # exclude = 'id'.split()


# class MoviesReviewsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie, Review
#         fields = '__all__'
