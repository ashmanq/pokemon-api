from io import BytesIO
import random
import requests
from PIL import Image
import base64
import re
import time
import random
import requests

POKEMON_API_URL = "https://pokeapi.co/api/v2"


# Function to check Pokemon ID against name
def check_pokemon_id_against_name(id, name):
    url = f"{POKEMON_API_URL}/pokemon/{id}"
    # response = requests.get(f"{POKEMON_API_URL}/pokemon/{id}")
    # result = response.json()
    result = api_call_with_exponential_backoff(url, "json")
    correct_pokemon_name = result["species"]["name"]
    correct_pokemon_url = result["sprites"]["other"]["official-artwork"][
        "front_default"
    ]
    return {
        "pokemonImage": correct_pokemon_url,
        "pokemonName": correct_pokemon_name,
        "result": correct_pokemon_name == name,
    }


# Function to get Pokemon image silhouette
def get_pokemon_image(image_url):
    response = api_call_with_exponential_backoff(image_url)
    img = Image.open(BytesIO(response.content))
    mask = img.getchannel("A")
    colored_layer = Image.new("RGBA", img.size, "#07679a")

    result = Image.alpha_composite(img, colored_layer)
    result.putalpha(mask)
    return encode_image_base64(result)


# Function that returns a game round with a Pokemon ID, 4 Pokemon options
# and an image outline
def get_game_round(pokemon_list, no_of_options, ignore_list=[]) -> list:
    options_list = get_random_list(pokemon_list, no_of_options, ignore_list)
    selected_pokemon = options_list[random.randrange(0, len(options_list))]

    # pokemon_details_response = requests.get(selected_pokemon.get("url"))
    # pokemon_details = pokemon_details_response.json()
    pokemon_details = api_call_with_exponential_backoff(selected_pokemon.get("url"), "json")
    selected_pokemon_index = pokemon_details.get("id")

    selected_pokemon_image_url = pokemon_details["sprites"]["other"][
        "official-artwork"
    ]["front_default"]
    selected_pokemon_image = get_pokemon_image(selected_pokemon_image_url)

    pokemon_options = map(return_name, options_list)

    round = {
        "pokemonOptions": list(pokemon_options),
        "selectedPokemonIndex": selected_pokemon_index,
        "pokemonImage": selected_pokemon_image,
    }
    return round


def get_pokemon_list(num_of_pokemon) -> list:
    url = f"{POKEMON_API_URL}/pokemon?limit={num_of_pokemon}"
    responseResult = api_call_with_exponential_backoff(url, "json")
    return responseResult.get("results", [])


def return_name(list) -> str:
    return list.get("name", "")


# Function takes in a list and returns a random sub list of random_list_length
def get_random_list(item_list, random_list_length, ignore_list=[]):
    list_length = len(item_list)
    if random_list_length > (list_length - len(ignore_list)):
        print("List size requested exceeds length of given list!")
        return None
    number_array = []
    results = []
    while len(number_array) < random_list_length:
        randNum = random.randrange(0, list_length)
        selectedItemId = re.search(
            r"/pokemon/(\d+)/$", item_list[randNum].get("url")
        ).group(1)
        if (randNum in number_array) == False and (
            int(selectedItemId) in ignore_list
        ) == False:
            number_array.append(randNum)
            results.append(item_list[randNum])
    return results


def encode_image_base64(img) -> str:
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)

    encoded_img = base64.b64encode(img_io.getbuffer()).decode("utf-8")
    return encoded_img

# Function to carry out API calls with exponential backoff
def api_call_with_exponential_backoff(url, response_type = "", max_retries = 3):
    retry_delay = 100/1000 # Get milliseconds
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if(response_type == "json"):
                return response.json()
            return response
        except requests.RequestException:
            print(f"Retrying after {retry_delay * 1000} milliseconds")
            time.sleep(retry_delay)
            retry_delay *= 2
            retry_delay += (random.uniform(0.001, .006)) # Adds jitter
        except Exception as e:
            print(str(e))
            
    raise Exception(f"Maximum retry attempts reached!")