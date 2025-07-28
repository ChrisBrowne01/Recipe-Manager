# Python Script: recipe_manager.py
import json
import os
from typing import Dict, List, Any

# 2. Define Recipe Data Structure
# - Decide on the structure of a recipe (e.g., title, ingredients, instructions).
# - Implement a data structure to represent a list that will hold all our recipe dictionaries in memory.
# Each dictionary will represent a single recipe.
# Example structure of a single recipe dictionary:
# {
#     "title": "Recipe Title",
#     "ingredients": ["Ingredient 1", "Ingredient 2"],
#     "instructions": "Step 1.\nStep 2."
# }

# Type alias for a single recipe dictionary
Recipe = Dict[str, Any]
# Type alias for the collection of recipes
Recipes = List[Recipe]

# --- 4. Define the directory for data files and full path ---
DATA_DIR = "data"
RECIPES_FILE = os.path.join(DATA_DIR, "recipes.json")

# --- File Handling Functions ---

def load_recipes() -> Recipes:
  os.makedirs(DATA_DIR, exist_ok=True)
  try:
      with open(RECIPES_FILE, "r") as file:
        return json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
      return []
  
def save_recipes(recipes: Recipes) -> None:
  os.makedirs(DATA_DIR, exist_ok=True)
  try:
      with open(RECIPES_FILE, "w") as file:
        json.dump(recipes, file, indent=4)
      print("Recipes saved successfully!")
  except IOError as e:
      print(f"Error saving recipes: {e}") 

# 3. Implement Recipe Management Functions
# - Implement functions to add, view, edit, and delete recipes.
def add_recipe(recipes: Recipes) -> None:
    print("\n--- Add a new recipe ---")
    title = input("Enter recipe title: ").strip()

    # Input Validation: Title must not be empty
    if not title:
      print("Title cannot be empty. Please try again.")
      return
    
    # Check for duplicate recipes
    for recipe in recipes:
      if recipe["title"].lower() == title.lower():
        print("Recipe already exists. Please try again.")
        return
    ingredients = []
    print("Enter ingredients one by one (type 'done' when finished and press Enter):")
    while True:
       ingredient = input(f"Ingredient {len(ingredients) + 1}: ").strip()
       if ingredient.lower() == 'done':
          break
       if ingredient:
          ingredients.append(ingredient)
    
    if not ingredients:
      print("A recipe must have atleast one ingredient. Aborting recipe.")
      return

    print("Enter instructions (type 'done' when finished and press Enter):")
    instructions_lines = []
    while True:
      line = input()
      if line.lower() == 'done':
        break
      instructions_lines.append(line)
    instructions = "\n".join(instructions_lines).strip()
       
    # Input Validation: Title must not be empty
    if not instructions:
      print("Recipe instructions cannot be empty. Aborting recipe addition.")
      return
    
    new_recipe = {
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions
    }

    recipes.append(new_recipe)
    print(f"Recipe '{title}' add successfully!")
    save_recipes(recipes)
# View all recipes
def view_recipes(recipes: Recipes) -> None:
    print("\n--- All Recipes ---")
    if not recipes:
      print("No recipes avalible.")
      return
    
    print(f"There are {len(recipes)} avalible recipe(s) listed below:")
    for i, recipe in enumerate(recipes):
      print(f"\n--- Recipe {i+1}: {recipe['title']} ---")
      print("Ingredients:")
      for ingredient in recipe['ingredients']:
        print(f"-{ingredient}")
      print("\nInstructions:")  
      print(recipe['instructions'])
      print("-" * (len(recipe['title']) + 14))

def search_recipes(recipes: Recipes) -> None:
   pass
def edit_recipe(recipes: Recipes) -> None:
   pass
def update_recipe(recipes: Recipes) -> None:
   pass
def delete_recipe(recipes: Recipes) -> None:
  pass
2
print(f"Recipe Manager System Initialized.")

# # Add initial recipe using the recipe's method
# add_recipe({"title": "Simple Tomato Pasta",
#     "ingredients": [
#         "200g pasta",
#         "1 can chopped tomatoes",
#         "2 cloves garlic, minced",
#         "1 tbsp olive oil",
#         "Salt and pepper to taste",
#         "Fresh basil for garnish (optional)"
#     ],
#     "instructions": """1. Bring a large pot of salted water to a boil. Add pasta and cook according to package directions.
# 2. While pasta cooks, heat olive oil in a pan over medium heat. Add minced garlic and cook until fragrant (about 1 minute).
# 3. Pour in chopped tomatoes. Season with salt and pepper. Simmer for 10-15 minutes, stirring occasionally.
# 4. Drain pasta, reserving about 1/2 cup of pasta water. Add drained pasta to the tomato sauce.
# 5. If sauce is too thick, add a splash of reserved pasta water until desired consistency is reached.
# 6. Serve hot, garnished with fresh basil if desired."""
# })

# Loop program
def main() -> None:
  recipes = load_recipes()
  while True:
    print("\n--- Welcome to the Recipe Manager! ---")
    print("Please enter an action from the options below:")
    print("1. Add a new recipe")
    print("2. View all recipes")
    print("3. Search for recipes")
    print("4. Edit a recipe")
    print("5. Delete a recipe")
    print("6. Exit Program\n")
    choice = input("Please enter your choice (1-6): ")
    if choice == "1":
        add_recipe(recipes)
    elif choice == "2":
        view_recipes(recipes)
    elif choice == "3":
        search_recipes(recipes)
    elif choice == "4":
        edit_recipe(recipes)
    elif choice == "5":
        delete_recipe(recipes)
    elif choice == "6":
        break
    else:
        print("Invalid choice. Please enter a number between (1-6)")

if __name__ == "__main__":
    main()