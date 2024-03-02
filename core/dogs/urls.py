from django.urls import path
from rest_framework import routers
from dogs.apps import DogsConfig

from dogs.views import DogViewSet, BreedListView, BreedDetailView, BreedCreateView, BreedUpdateView, BreedDeleteView

app_name = DogsConfig.name

router = routers.SimpleRouter()
router.register('dogs', DogViewSet)

urlpatterns = [
    path('', BreedListView.as_view()),
    path('<int:pk>/', BreedDetailView.as_view()),
    path('<int:pk>/update/', BreedUpdateView.as_view()),
    path('breed/create/', BreedCreateView.as_view()),
    path(' <int:pk>/delete/', BreedDeleteView.as_view()),
]

urlpatterns += router.urls