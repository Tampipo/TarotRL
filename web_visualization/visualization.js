let sessionData = null;
let currentGameIndex = 0;

function loadGame() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const loadedData = JSON.parse(e.target.result);

                if (loadedData.type === "session" && Array.isArray(loadedData.games)) {
                    sessionData = loadedData.games;
                    currentGameIndex = 0;
                    document.getElementById('game-navigation').style.display = 'flex';
                    displayCurrentGame();
                } else {
                    sessionData = null; // Clear any previous session data
                    document.getElementById('game-navigation').style.display = 'none';
                    displayGame(loadedData); // Display single game
                }
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

function displayCurrentGame() {
    if (sessionData && sessionData.length > 0) {
        displayGame(sessionData[currentGameIndex]);
        document.getElementById('current-game-display').textContent = `Game ${currentGameIndex + 1} of ${sessionData.length}`;
    }
}

function prevGame() {
    if (sessionData && currentGameIndex > 0) {
        currentGameIndex--;
        displayCurrentGame();
    }
}

function nextGame() {
    if (sessionData && currentGameIndex < sessionData.length - 1) {
        currentGameIndex++;
        displayCurrentGame();
    }
}
