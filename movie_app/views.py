from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, DirectorValidateSerializer, \
    MovieValidateSerializer, ReviewValidateSerializer
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

        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        name = serializer.validated_data.get('name')

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

        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(data={'director_id': director.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        print(request.query_params)
        # Step 1: Collect data of products from DB
        movies = Movie.objects \
            .select_related('director') \
            .prefetch_related('reviews').filter(title__contains=request.query_params.get('search_word', ''))

        # Step 2: Reformat(Serialize) of products
        data = MovieSerializer(movies, many=True).data

        # Step 3: Return data as JSON
        return Response(data=data)
    elif request.method == 'POST':

        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')

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

        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
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

        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text')
        movie_id = serializer.validated_data.get('movie_id')
        stars = serializer.validated_data.get('stars')

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

        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.stars = serializer.validated_data.get('stars')
        review.save()
        return Response(data={'review_id': review.id}, status=status.HTTP_201_CREATED)
