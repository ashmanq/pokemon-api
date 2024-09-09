from django.test import TestCase
from api.utils.pokemonutils import (
    get_random_list,
    get_game_round,
    check_pokemon_id_against_name,
)
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


class UtilsTestCase(TestCase):
    def setUp(self):
        self.pokemon_list = [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
            {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon/3/"},
            {"name": "charmander", "url": "https://pokeapi.co/api/v2/pokemon/4/"},
            {"name": "charmeleon", "url": "https://pokeapi.co/api/v2/pokemon/5/"},
            {"name": "charizard", "url": "https://pokeapi.co/api/v2/pokemon/6/"},
        ]
        self.test_name_and_id = [
            {"id": 1, "name": "bulbasaur"},
            {"id": 1, "name": "missingno"},
        ]
        self.client = APIClient()

    def test_get_random_list(self):
        """Function should generate an array of random pokemon"""
        random_array_length = 3
        num_array = get_random_list(self.pokemon_list, random_array_length)
        num_array_set = set()
        for item in num_array:
            num_array_set.add(item["name"])
        are_all_unique = len(num_array_set) == len(num_array)
        self.assertTrue(are_all_unique)
        self.assertEqual(random_array_length, len(num_array))

    def test_get_random_list_with_bad_inputs(self):
        """Function should return None if no of results exceeds range"""
        ran_array_length = 1000
        num_array = get_random_list(self.pokemon_list, ran_array_length)
        self.assertIsNone(num_array)

    def test_get_game_round(self):
        """Function should return a game round"""
        results = get_game_round(self.pokemon_list, 3)
        self.assertIsNotNone(results.get("pokemonOptions"))
        self.assertIsNotNone(results.get("selectedPokemonIndex"))
        self.assertIsNotNone(results.get("pokemonImage"))

    def test_can_check_id_against_name_is_correct(self):
        checkResult = check_pokemon_id_against_name(
            self.test_name_and_id[0].get("id"), self.pokemon_list[0].get("name")
        )
        self.assertTrue(checkResult)
        
    def test_can_check_id_against_name_is_incorrect(self):
        checkResult = check_pokemon_id_against_name(
            self.test_name_and_id[1].get("id"), self.pokemon_list[1].get("name")
        )
        self.assertFalse(checkResult)
