import unittest
import os
import json
from unittest.mock import patch, mock_open
import sys 

# Add the parent directory (project root) to the Python path
# This ensures that 'recipe_manager' can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..')) # Go up one level from 'tests'
sys.path.insert(0, project_root)

# Import all relevant functions and constants from your main script
from recipe_manager import add_recipe, view_recipes, search_recipes, edit_recipe, delete_recipe, load_recipes, save_recipes, RECIPES_FILE, DATA_DIR

class TestRecipeManager(unittest.TestCase):
    # This setup method runs before each test method
    def setUp(self):
        # Ensure the data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        # Define a path for a temporary test file
        self.test_file_path = RECIPES_FILE
        # Ensure the test file is clean before each test
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

        # Initialize an empty in-memory list for recipes for most tests.
        # Note: For tests that interact with file persistence, we'll use load_recipes/save_recipes directly.
        self.test_recipes_data = []

    # This teardown method runs after each test method
    def tearDown(self):
        # Clean up the test file after each test
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        # Optionally, remove the data directory if it's empty after tests
        if os.path.exists(DATA_DIR) and not os.listdir(DATA_DIR):
             os.rmdir(DATA_DIR)

    def test_load_recipes_empty_file(self):
        """Tests that load_recipes returns an empty list if the file doesn't exist."""
        recipes = load_recipes()
        self.assertEqual(recipes, [])

    def test_save_and_load_recipes(self):
        """Tests that recipes are correctly saved to and loaded from the file."""
        test_data = [
            {"title": "Saved Dish", "ingredients": ["Rice", "Water"], "instructions": "Cook rice with water."}
        ]
        save_recipes(test_data) # This saves to self.test_file_path
        loaded_data = load_recipes()
        self.assertEqual(loaded_data, test_data)

    # Patch 'save_recipes' to prevent actual file writes during add/edit/delete tests
    # We test save_recipes directly in test_save_and_load_recipes
    @patch('recipe_manager.save_recipes')
    def test_add_recipe_success(self, mock_save_recipes):
        """Tests adding a new recipe with valid input."""
        # Mock user input for add_recipe, providing each line separately
        with patch('builtins.input', side_effect=[
            'Test Title',
            'Ingredient One',
            'Ingredient Two',
            'done',
            'Instruction Line 1',
            'Instruction Line 2',
            'done'
        ]):
            add_recipe(self.test_recipes_data)
        
        self.assertEqual(len(self.test_recipes_data), 1)
        self.assertEqual(self.test_recipes_data[0]['title'], 'Test Title')
        self.assertEqual(self.test_recipes_data[0]['ingredients'], ['Ingredient One', 'Ingredient Two'])
        self.assertEqual(self.test_recipes_data[0]['instructions'], 'Instruction Line 1\nInstruction Line 2')
        mock_save_recipes.assert_called_once_with(self.test_recipes_data) # Check save was called

    @patch('recipe_manager.save_recipes')
    @patch('builtins.print') # Mock print to check output
    def test_add_recipe_empty_title(self, mock_print, mock_save_recipes):
        """Tests adding a recipe with an empty title."""
        with patch('builtins.input', side_effect=['']): # Empty title input
            add_recipe(self.test_recipes_data)
        self.assertEqual(len(self.test_recipes_data), 0) # No recipe added
        mock_print.assert_any_call("Title cannot be empty. Aborting recipe addition.")
        mock_save_recipes.assert_not_called()

    @patch('recipe_manager.save_recipes')
    @patch('builtins.print')
    def test_add_duplicate_recipe_title(self, mock_print, mock_save_recipes):
        """Tests adding a recipe with a title that already exists."""
        self.test_recipes_data.append({"title": "Existing Recipe", "ingredients": ["A"], "instructions": "B"})
        with patch('builtins.input', side_effect=['Existing Recipe']): # Try to add duplicate
            add_recipe(self.test_recipes_data)
        self.assertEqual(len(self.test_recipes_data), 1) # Should not add a new one
        mock_print.assert_any_call("A recipe with the title 'Existing Recipe' already exists. Please choose a different title or edit the existing recipe.")
        mock_save_recipes.assert_not_called()

    @patch('recipe_manager.save_recipes')
    @patch('builtins.print')
    def test_add_recipe_no_ingredients(self, mock_print, mock_save_recipes):
        """Tests adding a recipe without any ingredients."""
        with patch('builtins.input', side_effect=[
            'No Ingredient Recipe',
            'done', # No ingredients entered
            'Some Instructions',
            'done'
        ]):
            add_recipe(self.test_recipes_data)
        self.assertEqual(len(self.test_recipes_data), 0)
        mock_print.assert_any_call("A recipe must have atleast one ingredient. Aborting recipe.") # Fix typo here if you haven't already: "at least"
        mock_save_recipes.assert_not_called()

    @patch('recipe_manager.save_recipes')
    @patch('builtins.print')
    def test_add_recipe_empty_instructions(self, mock_print, mock_save_recipes):
        """Tests adding a recipe without any instructions."""
        with patch('builtins.input', side_effect=[
            'No Instruction Recipe',
            'Ing1',
            'done',
            'done' # No instructions entered
        ]):
            add_recipe(self.test_recipes_data)
        self.assertEqual(len(self.test_recipes_data), 0)
        mock_print.assert_any_call("Recipe instructions cannot be empty. Aborting recipe addition.")
        mock_save_recipes.assert_not_called()


    @patch('builtins.print')
    def test_view_recipes_empty(self, mocked_print):
        """Tests viewing recipes when the list is empty."""
        view_recipes(self.test_recipes_data)
        mocked_print.assert_any_call("No recipes available.")

    @patch('builtins.print')
    def test_view_recipes_multiple(self, mocked_print):
        """Tests viewing multiple recipes with correct formatting."""
        self.test_recipes_data.append({"title": "Recipe One", "ingredients": ["Flour", "Water"], "instructions": "Mix and bake."})
        self.test_recipes_data.append({"title": "Recipe Two", "ingredients": ["Sugar", "Milk"], "instructions": "Stir well."})

        view_recipes(self.test_recipes_data)

        # Check for specific call patterns that indicate correct formatting
        mocked_print.assert_any_call("\n--- All Recipes ---")
        mocked_print.assert_any_call("There are 2 available recipe(s) listed below:")
        mocked_print.assert_any_call("\n--- Recipe 1: Recipe One ---")
        mocked_print.assert_any_call("Ingredients:")
        mocked_print.assert_any_call("- Flour")
        mocked_print.assert_any_call("- Water")
        mocked_print.assert_any_call("\nInstructions:")
        mocked_print.assert_any_call("Mix and bake.")
        mocked_print.assert_any_call("\n--- Recipe 2: Recipe Two ---")
        mocked_print.assert_any_call("- Sugar")
        mocked_print.assert_any_call("- Milk")
        mocked_print.assert_any_call("Stir well.")


    @patch('builtins.print')
    @patch('builtins.input', side_effect=['Searchable']) # Mock input for search term
    def test_search_recipes_found_by_title(self, mock_input, mocked_print):
        """Tests searching for a recipe by title."""
        self.test_recipes_data.append({"title": "Searchable Recipe", "ingredients": ["X"], "instructions": "Y"})
        search_recipes(self.test_recipes_data) # No search_term argument here, it's prompted

        mocked_print.assert_any_call("Found 1 recipe(s) matching 'searchable':")
        mocked_print.assert_any_call("\n--- Found Recipe 1: Searchable Recipe ---")
        mocked_print.assert_any_call("Ingredients:")
        mocked_print.assert_any_call("- X")
        mocked_print.assert_any_call("\nInstructions:")
        mocked_print.assert_any_call("Y")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['butter']) # Mock input for search term
    def test_search_recipes_found_by_ingredient(self, mock_input, mocked_print):
        """Tests searching for a recipe by ingredient."""
        self.test_recipes_data.append({"title": "Cake Recipe", "ingredients": ["Flour", "Butter", "Eggs"], "instructions": "Bake it."})
        search_recipes(self.test_recipes_data)

        mocked_print.assert_any_call("Found 1 recipe(s) matching 'butter':")
        mocked_print.assert_any_call("\n--- Found Recipe 1: Cake Recipe ---")
        mocked_print.assert_any_call("- Flour")
        mocked_print.assert_any_call("- Butter")


    @patch('builtins.print')
    @patch('builtins.input', side_effect=['NonExistent']) # Mock input for search term
    def test_search_recipes_not_found(self, mock_input, mocked_print):
        """Tests searching for a recipe that does not exist."""
        self.test_recipes_data.append({"title": "Existing Recipe", "ingredients": ["A"], "instructions": "B"})
        search_recipes(self.test_recipes_data)
        mocked_print.assert_any_call("No recipes found matching 'nonexistent'.")

    @patch('recipe_manager.save_recipes')
    @patch('builtins.print')
    @patch('builtins.input', side_effect=[
        'Editable Recipe',  # Title to edit
        'New Edited Title', # New title
        'New Ingredient 1', # New ingredients
        'New Ingredient 2',
        'done',
        'Updated Instructions Line 1', # New instructions
        'Updated Instructions Line 2',
        'done'
    ])
    def test_edit_recipe_success(self, mock_input, mock_print, mock_save_recipes):
        """Tests successful editing of a recipe."""
        self.test_recipes_data.append({"title": "Editable Recipe", "ingredients": ["Old Ing"], "instructions": "Old Instr"})
        
        edit_recipe(self.test_recipes_data)
        
        self.assertEqual(self.test_recipes_data[0]['title'], 'New Edited Title')
        self.assertEqual(self.test_recipes_data[0]['ingredients'], ['New Ingredient 1', 'New Ingredient 2'])
        self.assertEqual(self.test_recipes_data[0]['instructions'], 'Updated Instructions Line 1\nUpdated Instructions Line 2')
        mock_print.assert_any_call("Recipe 'New Edited Title' updated successfully!")
        mock_save_recipes.assert_called_once_with(self.test_recipes_data)

    @patch('recipe_manager.save_recipes')
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['NonExistent Recipe'])
    def test_edit_recipe_not_found(self, mock_input, mock_print, mock_save_recipes):
        """Tests editing a recipe that doesn't exist."""
        self.test_recipes_data.append({"title": "Existing Recipe", "ingredients": ["A"], "instructions": "B"})
        edit_recipe(self.test_recipes_data)
        mock_print.assert_any_call("Recipe with title 'NonExistent Recipe' not found.")
        mock_save_recipes.assert_not_called()
        self.assertEqual(len(self.test_recipes_data), 1) # Should not have changed


    @patch('recipe_manager.save_recipes')
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['Deletable Recipe'])
    def test_delete_recipe_success(self, mock_input, mock_print, mock_save_recipes):
        """Tests successful deletion of a recipe."""
        self.test_recipes_data.append({"title": "Deletable Recipe", "ingredients": ["A"], "instructions": "B"})
        self.assertEqual(len(self.test_recipes_data), 1) # Ensure it starts with one

        delete_recipe(self.test_recipes_data)
        
        self.assertEqual(len(self.test_recipes_data), 0)
        mock_print.assert_any_call("Recipe 'Deletable Recipe' deleted successfully!")
        mock_save_recipes.assert_called_once_with(self.test_recipes_data)

    @patch('recipe_manager.save_recipes')
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['NonExistent Recipe'])
    def test_delete_recipe_not_found(self, mock_input, mock_print, mock_save_recipes):
        """Tests deleting a recipe that does not exist."""
        self.test_recipes_data.append({"title": "Existing Recipe", "ingredients": ["A"], "instructions": "B"})
        delete_recipe(self.test_recipes_data)
        mock_print.assert_any_call("Recipe with title 'NonExistent Recipe' not found.")
        mock_save_recipes.assert_not_called()
        self.assertEqual(len(self.test_recipes_data), 1) # Should not have changed


if __name__ == '__main__':
    unittest.main()