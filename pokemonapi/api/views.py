import requests
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render

from api.utils.pokemonutils import get_game_round, get_pokemon_list, check_pokemon_id_against_name

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
        return JsonResponse(pokemon_game_round)

    except requests.exceptions.RequestException as e:
        print("Error getting Pokemon: ", str(e))
        return JsonResponse({'error': "Error getting random Pokemon!" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def verify_pokemon(request):
    id = request.GET.get('id')
    name = request.GET.get('name')
    
    if(id == None or name == None):
        return JsonResponse({"error": "`id` and `name` request parameters are required!"}, status=status.HTTP_400_BAD_REQUEST)
    
    name = name.lower()
    
    try:
        checkResult = check_pokemon_id_against_name(id, name)
        return JsonResponse({'result': checkResult})
    except requests.exceptions.RequestException as e:
         print("Error verifying Pokemon: ", str(e))

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