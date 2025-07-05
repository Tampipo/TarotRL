function loadGame() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const gameData = JSON.parse(e.target.result);
                // Call the displayGame function from game_visualizer.js
                displayGame(gameData);
            } catch (error) {
                console.error("Error parsing JSON:", error);
                alert("Invalid JSON file.");
            }
        };
        reader.readAsText(file);
    } else {
        alert("Please select a JSON file.");
    }
}