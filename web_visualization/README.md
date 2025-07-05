# Web Visualization Package for TarotRL

This directory contains the web-based visualization tool for the Tarot game simulation. It allows for interactive replay and analysis of individual game sessions, displaying card movements, player hands, and trick progression.

## Contents

*   `visualization.html`: The main HTML file that serves as the user interface. It includes the necessary CSS styling and links to the JavaScript files.
*   `visualization.js`: A small JavaScript file that acts as the entry point for the visualization. It handles loading the game data from a JSON file and then delegates the display logic to `game_visualizer.js`.
*   `game_visualizer.js`: The core JavaScript file containing all the logic for parsing game data, rendering cards, managing the interactive navigation (tricks and plays), and reconstructing player hands.
*   `cards/`: This subdirectory holds all the image assets for the Tarot cards. The JavaScript code expects these images to follow a specific naming convention for correct display.

## How It Works

### Data Flow

1.  **Game Data Generation (Python):** The `simulate_game.py` script (located in the parent directory) runs a Tarot game and saves the game's complete state and history into a `game_log.json` file within this `web_visualization` directory.
2.  **Data Loading (JavaScript):** When `visualization.html` is opened (either automatically by `simulate_game.py` or manually), `visualization.js` prompts the user to load a `game_log.json` file. Once loaded, the JSON data is parsed into a JavaScript object.
3.  **Visualization Logic (JavaScript):** `game_visualizer.js` takes the parsed game data and dynamically generates the HTML elements to display the game information. It includes functions to:
    *   Parse card strings into structured data.
    *   Create HTML `<img>` elements for cards based on their names and the `cards/` directory's naming convention.
    *   Sort cards for consistent display in hands.
    *   Reconstruct player hands at any point in the game by tracking initial hands, discards, and played cards.
    *   Manage navigation through tricks and individual plays within a trick.
    *   Handle user interactions (button clicks, keyboard input).

### Card Naming Convention

For the card images in the `cards/` directory to display correctly, they must follow this naming convention:

*   **Suit Cards (Hearts, Diamonds, Clubs, Spades):** `[rank]-[suit_initial].png`
    *   Examples: `07-H.png` (7 of Hearts), `14-S.png` (King of Spades), `01-C.png` (1 of Clubs).
*   **Trump Cards:** `[rank]-T.png`
    *   Examples: `01-T.png` (Trump 1), `21-T.png` (Trump 21).
*   **Fool Card:** `00-T.png`

*(Note: All card images are expected to be in `.png` format. If you use a different format, you will need to adjust the `getImagePath` function in `game_visualizer.js` accordingly.)*

## Usage

To use this visualization tool:

1.  Ensure you have generated a `game_log.json` file by running `python simulate_game.py` from the project's root directory.
2.  Open `visualization.html` in your web browser (it should open automatically after running the Python script).
3.  Use the provided navigation buttons and keyboard arrow keys to explore the game.
