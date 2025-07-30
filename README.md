# Recipe Manager

## Project Overview

The Recipe Manager is a command-line application built with Python that allows users to manage their favorite recipes. It provides functionalities to add new recipes, view existing ones, search for recipes by title or ingredients, modify recipe details, and delete recipes. All recipe data is persistently stored in a JSON file, ensuring that your culinary creations are saved even after the application is closed.

## Features

* **Add Recipe:** Easily add new recipes by providing a title, a list of ingredients, and detailed instructions. The system prevents adding recipes with duplicate titles and ensures essential fields are not left empty.
* **View Recipes:** Display all stored recipes, neatly formatted with their ingredients and instructions.
* **Search Recipes:** Quickly find recipes by searching for keywords in their titles or ingredients.
* **Edit Recipe:** Update the title, ingredients, or instructions of an existing recipe.
* **Delete Recipe:** Remove unwanted recipes from your collection.
* **Data Persistence:** All recipe data is automatically saved to and loaded from a `recipes.json` file, ensuring no data loss between sessions.

## Project Structure

The project is organized into a clean and logical directory structure:

    ```text
    Recipe-Manager/
    ├── data/
    │   └── recipes.json      # Stores all recipe data
    ├── tests/
    │   ├── init.py           # Makes 'tests' a Python package
    │   └── test_recipe_manager.py # Unit tests for the application logic
    ├── README.md             # This documentation file
    └── recipe_manager.py     # The main application script
    ```

## How to Run the Application

### Prerequisites

* **Python 3.x:** Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation & Setup

1. **Clone the Repository:**

    If your project is on GitHub/GitLab, start by cloning it:

        ```bash
        git clone [https://github.com/ChrisBrowne01/Recipe-Manager.git](https://github.com/ChrisBrowne01/Recipe-Manager.git)
        cd Recipe-Manager
        ```

    If you've been working locally, simply navigate to your project's root directory:

        ```bash
        cd "C:\Users\Christina Browne\IT Online Learning\Python Essentials\Recipe-Manager"
        ```

2. **Ensure `data` directory exists:**

    The application will create the `data` directory and `recipes.json` file automatically if they don't exist when you run it, but you can create it manually if you prefer:

        ```bash
        mkdir data
        ```

### Execution

To start the Recipe Manager application, run the main script from the `Recipe-Manager` directory:

    ```bash
    python recipe_manager.py
    ```

Follow the on-screen prompts to interact with the application.

## How to Run Tests

The project includes a comprehensive suite of unit tests to ensure the reliability and correctness of the application's core functionalities.

### Test Execution

To run all unit tests, navigate to the `Recipe-Manager` directory and execute the following command:

    ```bash
    python -m unittest discover tests
    ```

You should see an "OK" message if all tests pass.

## Future Enhancements (Optional - but recommended to add a couple of ideas)

Here are some ideas for future improvements to the Recipe Manager:

* **User Interface:** Implement a graphical user interface (GUI) using libraries like Tkinter, PyQt, or a web-based interface using Flask or Django.
* **Categorization:** Allow recipes to be categorized (e.g., "Breakfast," "Dinner," "Dessert").
* **Scaling and Databases:** For larger recipe collections, migrate from JSON file storage to a more robust database system (e.g., SQLite, PostgreSQL).
* **Recipe Rating:** Implement a system for users to rate recipes.
* **Ingredient Management:** Track pantry inventory and suggest recipes based on available ingredients.
* **Export/Import:** Add functionality to export recipes to different formats (e.g., PDF, HTML) or import recipes from external sources.

## Usage

Upon running `recipe_manager.py`, you will be presented with a command-line interface. Follow the on-screen prompts to interact with the Recipe Manager.

## Author

* *Christina Browne*
* **Website Portfolio:** [https//:chrismbrowne.co.uk/](https://chrismbrowne.co.uk/)
* **GitHub Link:** [https://github.com/ChrisBrowne01](https://github.com/ChrisBrowne01)

## License

This project is open source and available under the [MIT License](LICENSE). *(Replace `LICENSE` with the actual license file if you create one.)*
