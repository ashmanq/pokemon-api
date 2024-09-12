# Pokemon API

## Instructions
To run locally you will need to have python installed

Once the repo is downloaded you will need to setup a Pythong environment for the first time using the following command:

```bash
python3 -m venv .venv
```

This will create a .env folder in your project directory. To start the project in this environment run:

```bash
source .venv/bin/activate
```

Once you have started the environment you will need to install the required Python libraries. From inside the shell environment run the following command:
```bash
pip install -r pokemonapi/requirements.txt
```

**Make sure you are in the home directory of the project when you do this.**

To then run the api cd into the project folder and use the following command (from inside the environment shell):

```bash
cd pokemonapi
python manage.py runserver
```

## End Points
There are two end points in this API

### Get Random Pokemon
Returns a random selection of pokemon along with a correct pokemon ID and silhouette

#### URL
`/pokemon/random`

#### Query Properties
You can send the following query properties:
- `noOfPokemon` - (Optional) The number of pokemon options to choose from (defaults to 4)
  
#### Response
This end point will return the following:
- `pokemonOptions` - a list of pokemon to select from
- `selectedPokemonIndex` - An index of the correct pokemon
- `pokemonImage` - Base64 data of the Pokemon silhouette
- `previousPokemonIds` - An array of IDs of previous played pokemon to ignore when getting new round
- `error` - Will be returned if any errors occurs in the request with a message

### Verify Pokemon
Takes an `id` and `name` and verifies if the chosen Pokemon is correct.

#### URL
`/pokemon/verify`

#### Query Properties
You can send the following query properties:
- `id` - (Required) ID of the correct Pokemon
- `name` - (Required) Name of the selected Pokemon
  
#### Response
This end point will return the following:
- `result` - A boolean result of either `true` or `false`
- `error` - Will be returned if any errors occurs in the request with a message

### API Documentation
This API uses Swagger for API documentation. You can view this on the API route: `api/schema/swagger-ui/` when the back end API is running.