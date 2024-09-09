import requests
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render

from api.utils.pokemonutils import get_game_round, get_pokemon_list

MAX_POKEMON = 400
# We cache the list of pokemon for the first request then reuse
pokemon_list_cache = []


def get_random_pokemon_game_round(request):
    no_of_pokemon = request.GET.get('noOfPokemon', 4)
    global pokemon_list_cache
    try:
        if(len(pokemon_list_cache) < MAX_POKEMON):
            pokemon_list_cache = get_pokemon_list(MAX_POKEMON)
            
        pokemon_game_round = get_game_round(pokemon_list_cache, int(no_of_pokemon))
        return JsonResponse({"result": pokemon_game_round})

    except requests.exceptions.RequestException as e:
        print("Error getting pokemon: ", str(e))
        return JsonResponse({'error': "Error getting random Pokemon!" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# Route for getting random pokemon for a game round
# API end point to get a random pokemon for a round
# First we need to get the pokemon list (150)
# Then we randomly select 4 pokemon from this list
# We then choose one pokemon that will be the correct pokemon
# We get the image of this pokemon
# We download the image and convert to one colour
# We send the following back:
#  - Correct Pokemon ID
#  - Four pokemon names
#  - Image of correct pokemon (altered)

# Route for verifying a pokemon
# We will receive a name and an ID
# We check the pokemon name by calling an endpoint with the id
# We extract the name from the result and check with the selected name
# We return a result