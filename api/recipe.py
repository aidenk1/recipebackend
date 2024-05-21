# Importing necessary libraries and modules
import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from auth_middleware import token_required  # Middleware for handling token authentication
from model.recipe import Recipe  # Importing the Recipe class from the model module

# Setting up a Blueprint for the recipe API
recipe_api = Blueprint('recipe_api', __name__, url_prefix='/api/recipe')
api = Api(recipe_api)  # Creating an API object associated with the Blueprint

class RecipeAPI:
    class _CRUD(Resource):
        def post(self):
            if request.is_json:
                data = request.get_json()
                # Extracting fields from the JSON data
                recipe_name = data.get('recipeName')
                recipe_instructions = data.get('recipeInstructions')
                recipe_ingredients = data.get('recipeIngredients')
                recommended_supplies = data.get('recommendedSupplies')
                recipe_thumbnail = data.get('recipeThumbnail')  # Extracting recipe_thumbnail from JSON data
                userid = data.get('userid')  # Extracting userid from JSON data
                

                # Creating a new Recipe object with the extracted data
                recipe = Recipe(
                    userid=userid,  # Passing userid to the Recipe constructor
                    name=recipe_name,
                    instruction=recipe_instructions,
                    ingredients=recipe_ingredients,
                    supplies=recommended_supplies,
                    thumbnail=recipe_thumbnail  # Passing recipe_thumbnail to the Recipe constructor
                )

                # Attempting to save the new recipe object to the database
                ro = recipe.create()

                # Checking if the recipe was successfully saved and returning the result
                if ro:
                    return jsonify(ro.read())
                return {'message': 'Failed to upload recipe'}, 500

            else:
                return {'message': 'Request body must be in JSON format'}, 400

        def get(self):
            recipes = Recipe.query.all()
            json_ready = [recipe.read() for recipe in recipes]
            return jsonify(json_ready)

        def put(self, recipe_id):
            try:
                recipe = Recipe.query.get(recipe_id)

                if not recipe:
                    return {'message': 'Recipe not found'}, 404

                if request.is_json:
                    data = request.get_json()

                    if 'recipeName' in data:
                        recipe.name = data['recipeName']
                    if 'recipeInstructions' in data:
                        recipe.instruction = data['recipeInstructions']
                    if 'recipeIngredients' in data:
                        recipe.ingredients = data['recipeIngredients']
                    if 'recommendedSupplies' in data:
                        recipe.supplies = data['recommendedSupplies']
                    if 'recipeThumbnail' in data:  # Allowing recipe_thumbnail to be updated
                        recipe.thumbnail = data['recipeThumbnail']
                    if 'userid' in data:  # Allowing userid to be updated
                        recipe.userid = data['userid']

                    recipe.update()  # Assuming there's an update method in Recipe class

                    return jsonify({'message': 'Recipe updated successfully', 'recipe': recipe.read()}), 200
                else:
                    return {'message': 'Request body must be in JSON format'}, 400
            except Exception as e:
                return {'message': f'Failed to update recipe: {str(e)}'}, 500

        # Placeholder for additional CRUD operations (PUT, DELETE, etc.)

    api.add_resource(_CRUD, '/')
