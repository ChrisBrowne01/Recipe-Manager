# Recipe Manager

---

## Project Objective

The **Recipe Manager** is a Python application designed to consolidate fundamental programming concepts such as data types, control flow, functions, file handling, and basic data manipulation. This project provides a practical platform for users to manage their recipes, offering functionalities to add, view, search, edit, and delete recipes.

---

## Features

* **Add Recipe**: Easily add new recipes with details like title, ingredients, and instructions.
* **View Recipes**: Display a list of all saved recipes.
* **Search Recipes**: Find recipes by title or ingredients.
* **Edit Recipe**: Modify existing recipe details.
* **Delete Recipe**: Remove recipes from the collection.
* **Persistent Storage**: Recipes are saved to and loaded from a file (text or JSON) to ensure data persistence between sessions.
* **Command-Line Interface (CLI)**: A simple and intuitive CLI guides users through the application's features.

---

## Getting Started

### Prerequisites

You will need Python installed on your system. This project is developed with Python 3.x.

### Installation

1. **Clone the repository (if applicable):**

    ```bash
    git clone <repository_url>
    cd Recipe-Manager
    ```

    (If not using Git, simply download the project files.)

2. **Project Structure:**

    Ensure your project directory is organized as follows:

    ```text
    Recipe-Manager/
    ├── recipe_manager.py
    └── data/
        └── recipes.json (or recipes.txt)
    ```

    The `data` directory will store your recipe information.

### How to Run

1. Navigate to the project's root directory in your terminal.
2. Run the main script:

    ```bash
    python recipe_manager.py
    ```

---

## Usage

Upon running `recipe_manager.py`, you will be presented with a command-line interface. Follow the on-screen prompts to interact with the Recipe Manager.

---

## Project Structure and Implementation Details

### 1. Recipe Data Structure

Recipes are stored using a suitable data structure (e.g., a dictionary or a custom class) to represent their title, a list of ingredients, and instructions.

### 2. Core Functionalities

Each primary action (add, view, search, edit, delete) is implemented as a separate function within `recipe_manager.py` for modularity and readability.

### 3. File Handling

Recipes are saved to and loaded from a file (preferably JSON for structured data) to ensure that your recipe collection is preserved across different uses of the application.

### 4. User Interface

A clear and simple command-line interface provides easy navigation and interaction.

### 5. Testing and Validation

The application includes robust input validation to handle invalid user inputs gracefully and prevent errors.

### 6. Documentation and Comments

The code is well-commented, providing insights into the logic and functionality of different parts of the application.

---

## Optional Enhancements (Bonus Features)

* **Recipe Categorization**: Implement categories for recipes (e.g., "Breakfast", "Dinner", "Dessert").
* **Recipe Ratings**: Allow users to assign ratings to recipes.
* **Enhanced UI**: Explore adding colors or ASCII art to the command-line interface for a more engaging experience.

---

## Challenges and Learnings

(*This section can be expanded during project presentation to discuss any challenges encountered and how they were overcome, e.g., handling file I/O errors, ensuring data integrity, or designing the user interface.*)

---

## Contributing

---

This project is a standalone exercise designed to showcase Python fundamentals.

---

## License

This project is open source and available under the [MIT License](LICENSE). *(Replace `LICENSE` with the actual license file if you create one.)*
