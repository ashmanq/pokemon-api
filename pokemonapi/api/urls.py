from django.urls import path
from . import views

urlpatterns = [
    path("pokemon/random/", views.get_random_pokemon_game_round, name="random-pokemon"),
]