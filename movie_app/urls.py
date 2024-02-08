from django.urls import path
from . import views
from .constants import LIST_CREATE, ITEM

urlpatterns = [
    # path('directors/', views.director_list_api_view),
    # path('directors/<int:id>/', views.director_detail_api_view),
    path('directors/', views.DirectorModelViewSet.as_view(LIST_CREATE)),
    path('directors/<int:id>', views.DirectorModelViewSet.as_view(ITEM)),
    # path('movies/', views.movie_list_api_view),
    # path('movies/<int:id>/', views.movie_detail_api_view),
    path('movies/', views.MovieListCreateAPIView.as_view()),
    path('movies/<int:id>/', views.movie_detail_api_view),
    # path('reviews/', views.review_list_api_view),
    # path('reviews/<int:id>/', views.review_detail_api_view),
    path('reviews/', views.ReviewModelViewSet.as_view(LIST_CREATE)),
    path('reviews/<int:id>/', views.ReviewModelViewSet.as_view(ITEM)),
]
