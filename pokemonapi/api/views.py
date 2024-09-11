import requests
import json
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.http import JsonResponse
from api.utils.pokemonutils import get_game_round, get_pokemon_list, check_pokemon_id_against_name

MAX_POKEMON = 150
# We cache the list of pokemon for the first request then reuse
pokemon_list_cache = []


class GetPokemonGameRound(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='noOfPokemon', location=OpenApiParameter.QUERY, description='Number of Pokemon name options to return', required=False, type=OpenApiTypes.INT),
            OpenApiParameter(name='previousPokemonIds', location=OpenApiParameter.QUERY, description="The previous correct Pokemon included here to ensure they aren't used again as a stringified array", required=False, type=OpenApiTypes.STR),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'pokemonOptions': {'type': 'array', 'items': {'type': 'string'}},
                    'selectedPokemonIndex': {'type': 'integer'},
                    'pokemonImage': {'type': 'string'},
                },
            },
            400: {
                'type': 'object',
                'properties': {'error': {'type': 'string'}}
            },
            500: {
                'type': 'object',
                'properties': {'error': {'type': 'string'}}
            }
        },
        auth=[],
        description="An end point that verifies a Pokemon name selected in a game round against the correct Pokemon's ID."
    )
    def get(self, request):
        global pokemon_list_cache
        no_of_pokemon = request.GET.get('noOfPokemon', 4)
        previous_pokemon_ids_string = request.GET.get('previousPokemonIds')
        print("IDs: ", previous_pokemon_ids_string)
        previous_pokemon_ids = []
        if(previous_pokemon_ids_string):
            previous_pokemon_ids = json.loads(previous_pokemon_ids_string)
        
        try:
            if(len(pokemon_list_cache) < MAX_POKEMON):
                pokemon_list_cache = get_pokemon_list(MAX_POKEMON)
                
            pokemon_game_round = get_game_round(pokemon_list_cache, int(no_of_pokemon), previous_pokemon_ids)
            return JsonResponse(pokemon_game_round)

        except Exception as e:
            print("Error getting Pokemon: ", str(e))
            return JsonResponse({'error': "Error getting random Pokemon!" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyPokemon(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', location=OpenApiParameter.QUERY, description='Pokemon ID to verify against', required=True, type=OpenApiTypes.STR),
            OpenApiParameter(name='name', location=OpenApiParameter.QUERY, description='Selected Pokemon name to verify', required=True, type=OpenApiTypes.STR),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'pokemonImage': {'type': 'string'},
                    'pokemonName': {'type': 'string'},
                    'result': {'type': 'boolean'},
                },
            },
            400: {
                'type': 'object',
                'properties': {'error': {'type': 'string'}}
            },
            500: {
                'type': 'object',
                'properties': {'error': {'type': 'string'}}
            }
        },
        auth=[],
        description="An end point that verifies a Pokemon name selected in a game round against the correct Pokemon's ID."
    )
    def get(self, request):
        id = request.GET.get('id')
        name = request.GET.get('name')
        
        if(id == None or name == None):
            return JsonResponse({'error': "`id` and `name` request parameters are required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        name = name.lower()
        
        try:
            checkResult = check_pokemon_id_against_name(id, name)
            return JsonResponse(checkResult)
        
        except Exception as e:
            print("Error verifying Pokemon: ", str(e))
            return JsonResponse({'error': "Error verifying Pokemon!" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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