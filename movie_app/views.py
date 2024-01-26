from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        # Step 1: Collect data of products from DB
        directors = Director.objects.all()

        # Step 2: Reformat(Serialize) of products
        data = DirectorSerializer(directors, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)
    elif request.method == 'POST':
        name = request.data.get('name')

        director = Director.objects.create(name=name)

        return Response(data={'director_id': director.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        director.name = request.data.get('name')
        director.save()
        return Response(data={'director_id': director.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        # Step 1: Collect data of products from DB
        movies = Movie.objects \
            .select_related('director') \
            .prefetch_related('reviews').all()

        # Step 2: Reformat(Serialize) of products
        data = MovieSerializer(movies, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')

        movie = Movie.objects.create(title=title, description=description,
                                     duration=duration, director_id=director_id)

        return Response(data={'movie_id': movie.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
        movie.save()
        return Response(data={'movie_id': movie.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        # Step 1: Collect data of products from DB
        reviews = Review.objects.all()

        # Step 2: Reformat(Serialize) of products
        data = ReviewSerializer(reviews, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)
    elif request.method == 'POST':
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        stars = request.data.get('stars')

        review = Review.objects.create(text=text, movie_id=movie_id, stars=stars)

        return Response(data={'review_id': review.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.movie_id = request.data.get('movie_id')
        review.stars = request.data.get('stars')
        review.save()
        return Response(data={'review_id': review.id}, status=status.HTTP_201_CREATED)
