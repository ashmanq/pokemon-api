from django.urls import path
from . import views

urlpatterns = [
    path("pokemon/random/", views.GetPokemonGameRound.as_view(), name="random-pokemon"),
    path("pokemon/verify/", views.VerifyPokemon.as_view(), name="verify-pokemon"),
]