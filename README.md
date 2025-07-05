# TarotRL Project: Web Visualization Tool

This `README.md` provides an overview of the web-based visualization tool for the Tarot game simulation, with a focus on understanding the JavaScript code.

## Project Overview

The `TarotRL` project simulates a Tarot card game. The web visualization tool allows you to replay and analyze individual games, observing the flow of cards, player hands, and trick progression.

## How to Use the Visualization Tool

1.  **Generate a Game Log:**
    Run the Python simulation script from the project root directory:
    ```bash
    python simulate_game.py
    ```
    This will run a single game, save its data to `web_visualization/game_log.json`, and automatically open the visualization in your default web browser.

2.  **Load Game Data (if not opened automatically or for a different file):**
    *   Open `web_visualization/visualization.html` in your web browser.
    *   Click the "Load Game" button and select the `game_log.json` file (located in `web_visualization/`).

3.  **Navigate the Game:**
    *   **Toggle Game Setup Info:** Click the "Toggle Game Setup Info" button to show/hide initial hands, bids, chien, and final scores.
    *   **Trick Navigation:** Use the "Previous Trick" and "Next Trick" buttons to move between different tricks in the game.
    *   **Play Navigation:** Use the "Previous Play" and "Next Play" buttons (or **left/right arrow keys** on your keyboard) to step through each card played within the current trick. This shows the cards on the table, the current player's hand, and the card they played.

## Code Structure (Web Visualization)

The web visualization components are located in the `web_visualization/` directory:

*   `web_visualization/visualization.html`: The main HTML file that provides the user interface (buttons, display areas) and links to the JavaScript and CSS.
*   `web_visualization/visualization.js`: A small JavaScript file that acts as the entry point. Its primary role is to handle the file input and trigger the loading and display of game data using functions from `game_visualizer.js`.
*   `web_visualization/game_visualizer.js`: This is the core JavaScript file containing all the logic for parsing game data, rendering cards, and managing the interactive visualization.
*   `web_visualization/cards/`: This directory contains the image assets for the Tarot cards. The JavaScript expects these images to follow a specific naming convention.

### Key Functions in `game_visualizer.js`

*   `parseCardString(cardString)`: Takes a card string (e.g., "7 of Hearts", "21 of Trump", "Fool") and parses it into an object with `rank` and `suit` properties. This is crucial for mapping to image filenames.
*   `createCardElement(cardString)`: Generates an HTML `div` element representing a card. It creates an `<img>` tag whose `src` is determined by `getImagePath`. If the image fails to load, it falls back to displaying the card string as text.
*   `getImagePath(cardInfo)`: Constructs the file path for a card image based on its rank and suit, adhering to the naming convention in the `cards/` directory. It handles suit cards, trump cards, and the Fool.
    *   **Card Naming Convention:** Your card images should be named as `[rank]-[suit_initial].png` (e.g., `07-H.png` for 7 of Hearts, `14-S.png` for King of Spades, `05-T.png` for Trump 5). The Fool card is `00-T.png`.
*   `sortCards(cards)`: Sorts an array of card strings according to Tarot rules (Fool lowest, then Trumps by rank, then suits by rank within suit, and finally by a defined suit order). This ensures hands are displayed consistently.
*   `reconstructPlayerHand(playerName, trickIndex, playIndex)`: This is a complex function that calculates a player's hand at a specific moment in the game. It starts with the initial hand, adds chien cards if the player was the taker, and then removes cards that have been discarded or played in previous tricks or earlier plays within the current trick.
*   `displayGame(gameData)`: The main function called after a JSON game log is loaded. It populates the "Game Setup Info" section and initializes the display of the first trick and first play.
*   `displayTrick(index)`: Updates the display to show a specific trick. It resets the `currentPlayIndex` to 0 and calls `displayCurrentPlay`.
*   `displayCurrentPlay()`: Renders the details of the current play within a trick. It shows cards on the table, the current player, the card they played, and their reconstructed hand.
*   `prevTrick()`, `nextTrick()`, `prevPlay()`, `nextPlay()`: Functions to navigate through tricks and plays. `prevPlay()` and `nextPlay()` also handle transitioning between tricks when reaching the beginning or end of a trick's plays.
*   `toggleGameInfo()`: Toggles the visibility of the "Game Setup Info" section using a CSS class.

## Key JavaScript Concepts Used

*   **DOM Manipulation:** JavaScript interacts with the HTML elements (Document Object Model) to dynamically update content, create new elements (like card `div`s and `img`s), and modify their properties (e.g., `innerHTML`, `classList`).
*   **Event Listeners:** Functions like `loadGame()`, `toggleGameInfo()`, `prevTrick()`, `nextTrick()`, `prevPlay()`, `nextPlay()` are triggered by user interactions (button clicks, keyboard presses). The `document.addEventListener('keydown', ...)` sets up a listener for keyboard events.
*   **JSON Parsing:** The `JSON.parse()` method is used to convert the text content of the `game_log.json` file into a JavaScript object that can be easily accessed and manipulated.
*   **CSS Styling:** CSS rules (defined in `visualization.html`'s `<style>` block) control the visual appearance of the elements, including card size, layout (using `display: flex`), and hiding/showing sections.

## Future Improvements

*   **More Sophisticated Card Rendering:** Add card backs, animations for playing cards, or drag-and-drop functionality.
*   **Game Playback Controls:** Add a play/pause button and a speed control for automatic playback.
*   **Player Information:** Display more details about each player (e.g., AI type, score in current game).
*   **Error Handling:** More robust error handling for missing images or malformed JSON.
*   **Styling:** Improve the overall visual design and responsiveness.
