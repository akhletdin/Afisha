from rest_framework import serializers
from .models import Director, Movie, Review
from rest_framework.exceptions import ValidationError


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

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=20)
    description = serializers.CharField(required=False)
    duration = serializers.FloatField(min_value=5, max_value=100000)
    director_id = serializers.IntegerField()

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director not found!')
        return director_id


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=15)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100)
    movie_id = serializers.IntegerField()
    stars = serializers.IntegerField()
