from django.test import TestCase
from django.urls import reverse
from api.utils.pokemonutils import (
    get_random_list,
    get_game_round,
    check_pokemon_id_against_name,
    return_name,
)
from rest_framework.test import APIClient

# Create your tests here.


class APITestCase(TestCase):
    def setUp(self) -> None:
        self.pokemon_list = [
            {"name": "raichu", "url": "https://pokeapi.co/api/v2/pokemon/26/"},
            {"name": "sandshrew", "url": "https://pokeapi.co/api/v2/pokemon/27/"},
            {"name": "sandslash", "url": "https://pokeapi.co/api/v2/pokemon/28/"},
            {"name": "nidoran-f", "url": "https://pokeapi.co/api/v2/pokemon/29/"},
        ]
        self.client = APIClient()
        
    def test_can_get_round_from_api_end_point(self):
        url = reverse('random-pokemon')
        response = self.client.get(url)
        results = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(results.get("pokemonOptions"))
        self.assertIsNotNone(results.get("selectedPokemonIndex"))
        self.assertIsNotNone(results.get("pokemonImage"))
        
    def test_can_verify_pokemon_selection_from_api_end_point_and_get_false(self):
        url = reverse('verify-pokemon')
        response = self.client.get(url, QUERY_STRING="id=1&name=YO")
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(False, result.get('result'))
        self.assertTrue(result.get('pokemonName') == 'bulbasaur')
        
    def test_can_verify_pokemon_selection_from_api_end_point_and_get_true(self):
        url = reverse('verify-pokemon')
        response = self.client.get(url, {'id': 1, 'name': 'bulbasaur'})
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True, result.get('result'))
        
    def test_can_verify_pokemon_selection_and_get_404_when_no_inputs(self):
        url = reverse('verify-pokemon')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        


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
        
    def test_random_list_shouldnt_contain_anything_in_ignore_list(self):
        random_array_length = 3
        ignore_list = [4, 5, 6]
        num_array = get_random_list(self.pokemon_list, random_array_length, ignore_list)
        num_array_names = []
        for item in num_array:
            num_array_names.append(item["name"])
        self.assertFalse('charmander' in num_array_names)
        self.assertFalse('charmeleon' in num_array_names)
        self.assertFalse('charizard' in num_array_names)

    def test_get_random_list_with_bad_inputs(self):
        """Function should return None if no of results exceeds range"""
        ran_array_length = 1000
        num_array = get_random_list(self.pokemon_list, ran_array_length)
        self.assertIsNone(num_array)

    def test_can_check_id_against_name_is_correct(self):
        checkResult = check_pokemon_id_against_name(
            self.test_name_and_id[0].get("id"), self.pokemon_list[0].get("name")
        )
        self.assertTrue(checkResult.get('result'))

    def test_can_check_id_against_name_is_incorrect(self):
        checkResult = check_pokemon_id_against_name(
            self.test_name_and_id[1].get("id"), self.pokemon_list[1].get("name")
        )
        self.assertFalse(checkResult.get('result'))
        
    def test_get_game_round(self):
        """Function should return a game round"""
        results = get_game_round(self.pokemon_list, 3)
        self.assertIsNotNone(results.get("pokemonOptions"))
        self.assertIsNotNone(results.get("selectedPokemonIndex"))
        self.assertIsNotNone(results.get("pokemonImage"))
