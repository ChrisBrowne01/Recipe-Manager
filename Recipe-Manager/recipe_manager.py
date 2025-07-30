"""
Recipe Manager Application

This script provides a command-line interface for managing recipes.
It allows users to add, view, search, edit, and delete recipes,
with all data persisting to a JSON file.

Key functionalities include:
- Data storage in a JSON file for persistence.
- Validation for user inputs to ensure data integrity.
- Clear menu-driven interaction for ease of use.
"""
import json
import os
from typing import Dict, List, Any

# 2. Define Recipe Data Structure
# - Structure recipe data as JSON using, title, and instructions.
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
DATA_DIR = "Recipe-Manager\data" # "data" is if Recipe-Manager is the root directory, as the root is the level above it, path should be "Recipe-Manager\data"
RECIPES_FILE = os.path.join(DATA_DIR, "recipes.json")

# --- File Handling Functions ---

def load_recipes() -> Recipes:
    """
    Loads recipes from the JSON file.

    If the file does not exist or is empty/corrupt, it initializes an empty list.

    Returns:
        Recipes: A list of recipe dictionaries loaded from the file.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(RECIPES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
  
def save_recipes(recipes: Recipes) -> None:
    """
    Saves the current list of recipes to the JSON file.

    Args:
        recipes (Recipes): The list of recipe dictionaries to save.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(RECIPES_FILE, "w") as file:
            json.dump(recipes, file, indent=4)
        print("Recipes saved successfully!")
    except IOError as e:
        print(f"Error saving recipes: {e}") 

# 3. Implement Recipe Management Functions: add, view, edit, and delete recipes.
# Adds a new recipe
def add_recipe(recipes: Recipes) -> None:
    """
    Prompts the user for recipe details and adds a new recipe to the list.

    Includes validation for title (not empty, no duplicates),
    ingredients (at least one), and instructions (not empty).

    Args:
        recipes (Recipes): The current list of recipe dictionaries to which the new recipe will be added.
    """
    print("\n--- Add a new recipe ---")
    title = input("Enter recipe title: ").strip()

    # Input Validation: Title must not be empty
    if not title:
        print("Title cannot be empty. Aborting recipe addition.")
        return
    
    # Check for duplicate titles (case-insensitive)
    for recipe in recipes:
        if recipe["title"].lower() == title.lower():
            print(f"A recipe with the title '{title}' already exists. Please choose a different title or edit the existing recipe.")
            return

    ingredients = []
    print("Enter ingredients one by one (type 'done' on an empty line when finished and press Enter):") # Clarified instruction
    while True:
        ingredient = input(f"Ingredient {len(ingredients) + 1}: ").strip()
        if ingredient.lower() == 'done':
            break
        if ingredient: # Only add non-empty ingredients
            ingredients.append(ingredient)
    
    if not ingredients:
        print("A recipe must have atleast one ingredient. Aborting recipe.")
        return

    print("Enter instructions (type 'done' on an empty line by itself when finished and press Enter): ") # Clarified instruction
    instructions_lines = []
    while True:
        line = input()
        if line.lower() == 'done':
            break
        instructions_lines.append(line)
    instructions = "\n".join(instructions_lines).strip()
       
    # Input Validation: Instructions must not be empty
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
    save_recipes(recipes) # Save immediately after adding

# View all recipes
def view_recipes(recipes: Recipes) -> None:
    """
    Displays all recipes currently loaded, including their ingredients and instructions.

    If no recipes are available, it prints a corresponding message.

    Args:
        recipes (Recipes): The list of recipe dictionaries to display.
    """
    print("\n--- All Recipes ---")
    if not recipes:
        print("No recipes available.")
        return
    
    print(f"There are {len(recipes)} available recipe(s) listed below:")
    for i, recipe in enumerate(recipes):
        print(f"\n--- Recipe {i+1}: {recipe['title']} ---")
        print("Ingredients:")
        for ingredient in recipe['ingredients']:
            print(f"- {ingredient}")
        print("\nInstructions:")  
        print(recipe['instructions'])
        print("-" * (len(recipe['title']) + 14))

# Search by title or ingredients
def search_recipes(recipes: Recipes) -> None:
    """
    Searches for recipes by matching a search term against recipe titles or ingredients.

    Displays all recipes that contain the search term (case-insensitive).

    Args:
        recipes (Recipes): The list of recipe dictionaries to search through.
    """
    print("\n--- Search Recipes ---")
    if not recipes:
        print("No recipes available to search.")
        return

    search_term = input("Enter title or ingredient to search for: ").strip().lower()
    if not search_term:
        print("Search term cannot be empty.")
        return

    found_recipes = []
    for recipe in recipes:
        # Search by title
        if search_term in recipe["title"].lower():
            found_recipes.append(recipe)
            continue # Move to the next recipe once found by title

        # Search by ingredients
        for ingredient in recipe["ingredients"]:
            if search_term in ingredient.lower():
                found_recipes.append(recipe)
                break # Found in ingredients, no need to check other ingredients of this recipe
      
    if not found_recipes:
        print(f"No recipes found matching '{search_term}'.")
    else:
        print(f"Found {len(found_recipes)} recipe(s) matching '{search_term}':")
        for i, recipe in enumerate(found_recipes):
            print(f"\n--- Found Recipe {i+1}: {recipe['title']} ---")
            print("Ingredients:")
            for ingredient in recipe['ingredients']:
                print(f"- {ingredient}")
            print("\nInstructions:")
            print(recipe['instructions'])
            print("-" * (len(recipe['title']) + 18))

def edit_recipe(recipes: Recipes) -> None:
    """
    Edits an existing recipe by its title.

    Allows the user to modify the title, ingredients, and instructions.
    Users can keep existing values by pressing Enter without typing new input.

    Args:
        recipes (Recipes): The list of recipe dictionaries to modify.
    """
    print("\n--- Edit Recipe ---")
    if not recipes:
        print("No recipes available to edit.")
        return

    view_recipes(recipes) # First, list recipes so the user knows what to edit
    title_to_edit = input("\nEnter the TITLE of the recipe you want to edit: ").strip()

    # Find the recipe
    recipe_found = None
    for i, recipe in enumerate(recipes):
        if recipe["title"].lower() == title_to_edit.lower():
            recipe_found = recipe
            recipe_index = i # Keep track of the index for duplicate title check on edit
            break

    if not recipe_found:
        print(f"Recipe with title '{title_to_edit}' not found.")
        return

    print(f"\nEditing recipe: '{recipe_found['title']}'")
    print("Enter new details (press Enter to keep current value):")

    # Edit Title
    new_title = input(f"New Title (Current: {recipe_found['title']}): ").strip()
    if new_title:
        # Check for duplicate new title, excluding the current recipe being edited
        is_duplicate = False
        for i, r in enumerate(recipes):
            if i != recipe_index and r["title"].lower() == new_title.lower():
                print(f"Error: A recipe with the title '{new_title}' already exists. Title not updated.")
                is_duplicate = True
                break
        if not is_duplicate:
            recipe_found["title"] = new_title

    # Edit Ingredients
    print("\n--- Edit Ingredients ---")
    print("Current Ingredients:")
    for i, ing in enumerate(recipe_found['ingredients']):
        print(f"{i+1}. {ing}")

    new_ingredients = []
    print("Enter new ingredients one by one (type 'done' on an empty line when finished).")
    print("To remove an ingredient, simply don't re-enter it.")
    print("To keep existing ingredients, type them again or re-enter 'done' immediately.")
    while True:
        ingredient = input(f"New Ingredient {len(new_ingredients) + 1} (or 'done'): ").strip()
        if ingredient.lower() == 'done':
            break
        if ingredient:
            new_ingredients.append(ingredient)

    if new_ingredients: # Only update if new ingredients were provided
        recipe_found['ingredients'] = new_ingredients
    else:
        # Give option to clear ingredients or keep existing if user just types 'done'
        if input("No new ingredients entered. Clear all current ingredients? (yes/no): ").lower() == 'yes':
            recipe_found['ingredients'] = []
            print("Ingredients cleared.")
        else:
            print("Keeping original ingredients.")

    # Edit Instructions
    print("\n--- Edit Instructions ---")
    print("Current Instructions:")
    print(recipe_found['instructions'])
    print("Enter new instructions (type 'done' on an empty line by itself when finished).")
    print("Press Enter immediately to keep current instructions.")

    new_instructions_lines = []
    while True:
        line = input()
        if line.lower() == 'done':
            break
        new_instructions_lines.append(line)

    if new_instructions_lines: # Only update if new instructions were provided
        new_instructions = "\n".join(new_instructions_lines).strip()
        if new_instructions: # Make sure the new instructions aren't just empty
            recipe_found['instructions'] = new_instructions
        else:
            print("New instructions were empty. Keeping original instructions.")
    else:
        print("Keeping original instructions.")

    print(f"Recipe '{recipe_found['title']}' updated successfully!")
    save_recipes(recipes) # Save immediately after editing

def delete_recipe(recipes: Recipes) -> None:
    """
    Deletes a recipe from the list by its title.

    Args:
        recipes (Recipes): The list of recipe dictionaries to delete from.
    """
    print("\n--- Delete Recipe ---")
    if not recipes:
        print("No recipes available to delete.")
        return

    view_recipes(recipes) # Show recipes so user knows what to delete
    title_to_delete = input("\nEnter the TITLE of the recipe you want to delete: ").strip()

    initial_len = len(recipes)
    # Using a list comprehension to rebuild the list without the deleted item
    recipes[:] = [recipe for recipe in recipes if recipe["title"].lower() != title_to_delete.lower()]

    if len(recipes) < initial_len:
        print(f"Recipe '{title_to_delete}' deleted successfully!")
        save_recipes(recipes) # Save immediately after deleting
    else:
        print(f"Recipe with title '{title_to_delete}' not found.")

# --- 5. User Interface (Main Application Loop) ---

print(f"Recipe Manager System Initialized.")

# Loop program
def main() -> None:
  """
  The main function that runs the Recipe Manager application.

  It loads existing recipes, displays the main menu, and handles
  user interactions by calling the appropriate recipe management functions.
  """
  recipes = load_recipes() # Load recipes at the start of the program

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
            print("Exiting Recipe Manager. Goodbye!")
            break # Exsit the loop
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

# This ensures main() is called only when the script is executed directly
if __name__ == "__main__":
    main()
