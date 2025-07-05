let gameDataGlobal;
let currentTrickIndex = 0;
let currentPlayIndex = 0;

function parseCardString(cardString) {
    if (cardString === "Fool") {
        return { rank: "Fool", suit: "Fool" };
    }
    const parts = cardString.split(" of ");
    if (parts.length === 2) {
        return { rank: parts[0], suit: parts[1].toLowerCase() };
    }
    return { rank: cardString, suit: "unknown" }; // Fallback
}

function createCardElement(cardString) {
    const cardInfo = parseCardString(cardString);
    const cardDiv = document.createElement('div');
    cardDiv.classList.add('card', cardInfo.suit);

    const img = document.createElement('img');
    img.src = getImagePath(cardInfo);
    img.alt = cardString; // Alt text for accessibility
    img.onerror = function() {
        // Fallback to text if image not found
        this.parentNode.innerHTML = `<div style="color: black;">${cardString}</div>`; // Simple text fallback
    };

    cardDiv.appendChild(img);
    return cardDiv;
}

function getImagePath(cardInfo) {
    const base_path = 'cards/';
    let filename;

    // Map suit names from JSON to file naming convention
    const suitToFileMap = {
        'hearts': 'H',
        'diamonds': 'D',
        'clubs': 'C',
        'spades': 'S',
        'trump': 'T'
    };

    if (cardInfo.suit === 'fool') {
        filename = '00-T.png'; // Assuming 00-T.png is the Fool
    } else if (cardInfo.suit === 'trump') {
        // Trump cards are 1-21, so rank is directly used
        filename = `${String(cardInfo.rank).padStart(2, '0')}-T.png`;
    } else {
        // Suit cards (Hearts, Diamonds, Clubs, Spades)
        const suitInitial = suitToFileMap[cardInfo.suit];
        // Ranks are 1-14 for suits
        filename = `${String(cardInfo.rank).padStart(2, '0')}-${suitInitial}.png`;
    }
    return base_path + filename;
}

function sortCards(cards) {
    const suitOrder = {
        "hearts": 0,
        "diamonds": 1,
        "clubs": 2,
        "spades": 3,
    };

    return cards.sort((a, b) => {
        const cardA = parseCardString(a);
        const cardB = parseCardString(b);

        // Fool is always lowest
        if (cardA.suit === "fool") return -1;
        if (cardB.suit === "fool") return 1;

        // Trump cards are higher than suit cards
        if (cardA.suit === "trump" && cardB.suit !== "trump") return 1;
        if (cardA.suit !== "trump" && cardB.suit === "trump") return -1;

        // Sort within Trump
        if (cardA.suit === "trump" && cardB.suit === "trump") {
            return parseInt(cardA.rank) - parseInt(cardB.rank);
        }

        // Sort within suits
        if (cardA.suit === cardB.suit) {
            return parseInt(cardA.rank) - parseInt(cardB.rank);
        }

        // Sort by suit order
        return suitOrder[cardA.suit] - suitOrder[cardB.suit];
    });
}


function reconstructPlayerHand(playerName, trickIndex, playIndex) {
    let hand = [];

    // Start with initial hand
    if (gameDataGlobal.initial_hands[playerName]) {
        hand = [...gameDataGlobal.initial_hands[playerName]];
    }

    // Account for chien cards if player is the taker and bid was Petite or Garde
    if (gameDataGlobal.bid_phase.taker === playerName) {
        const finalBid = gameDataGlobal.bid_phase.final_bid;
        // In Python, Bid.GARDE_SANS is 3. Petite is 1, Garde is 2.
        // So, if finalBid is 'Petite' or 'Garde', the chien is added to hand.
        if (finalBid === 'Petite' || finalBid === 'Garde') {
            hand.push(...gameDataGlobal.chien);
        }
    }

    // Account for discarded cards by taker
    if (gameDataGlobal.bid_phase.taker === playerName && gameDataGlobal.discard_phase.taker_discarded_cards) {
        for (const discardedCard of gameDataGlobal.discard_phase.taker_discarded_cards) {
            const index = hand.indexOf(discardedCard);
            if (index > -1) {
                hand.splice(index, 1);
            }
        }
    }

    // Account for cards played in previous tricks
    for (let t = 0; t < trickIndex; t++) {
        const trick = gameDataGlobal.tricks[t];
        for (const cardPlayed of trick.cards_played) {
            if (cardPlayed.player === playerName) {
                const index = hand.indexOf(cardPlayed.card);
                if (index > -1) {
                    hand.splice(index, 1);
                }
            }
        }
    }

    // Account for cards played in the current trick up to the current play index
    const currentTrick = gameDataGlobal.tricks[trickIndex];
    for (let p = 0; p < playIndex; p++) {
        const cardPlayed = currentTrick.cards_played[p];
        if (cardPlayed.player === playerName) {
            const index = hand.indexOf(cardPlayed.card);
            if (index > -1) {
                hand.splice(index, 1);
            }
        }
    }

    return hand;
}

function displayGame(gameData) {
    gameDataGlobal = gameData;
    currentTrickIndex = 0; // Reset to first trick
    currentPlayIndex = 0; // Reset to first play

    const gameInfoDiv = document.getElementById('game-info');

    gameInfoDiv.innerHTML = `
        <h2>Game ID: ${gameData.game_id}</h2>
        <p><strong>Dealer:</strong> ${gameData.dealer}</p>
        <p><strong>Players:</strong> ${gameData.players.map(p => p.name).join(', ')}</p>
        <h3>Initial Hands:</h3>
        <ul>
            ${Object.entries(gameData.initial_hands).map(([player, hand]) => `
                <li><strong>${player}:</strong> ${sortCards(hand).map(createCardElement).map(el => el.outerHTML).join('')}</li>
            `).join('')}
        </ul>
        <h3>Chien:</h3>
        <p><div class="card-display-row">${sortCards(gameData.chien).map(createCardElement).map(el => el.outerHTML).join('')}</div></p>
        <h3>Bid Phase:</h3>
        <p><strong>Taker:</strong> ${gameData.bid_phase.taker || 'None'}</p>
        <p><strong>Final Bid:</strong> ${gameData.bid_phase.final_bid || 'None'}</p>
        <h4>Bids:</h4>
        <ul>
            ${gameData.bid_phase.bids.map(bid => `
                <li>${bid.player}: ${bid.bid}</li>
            `).join('')}
        </ul>
        <h3>Discard Phase:</h3>
        <p><strong>Taker Discarded Cards:</strong> <div class="card-display-row">${gameData.discard_phase.taker_discarded_cards ? sortCards(gameData.discard_phase.taker_discarded_cards).map(createCardElement).map(el => el.outerHTML).join('') : 'None'}</div></p>
        <h3>Final Scores:</h3>
        <ul>
            ${Object.entries(gameData.final_scores).map(([key, value]) => `
                <li><strong>${key.replace(/_/g, ' ')}:</strong> ${value}</li>
            `).join('')}
        </ul>
    `;
    gameInfoDiv.classList.add('hidden'); // Ensure it's hidden after loading

    // Initialize trick and play display
    displayTrick(currentTrickIndex);
}

function displayTrick(index) {
    const currentTrickDisplay = document.getElementById('current-trick-display');

    if (!gameDataGlobal || !gameDataGlobal.tricks || gameDataGlobal.tricks.length === 0) {
        currentTrickDisplay.textContent = 'Trick 0/0';
        document.getElementById('current-trick-container').innerHTML = '<p>No tricks to display.</p>';
        document.getElementById('play-navigation').style.display = 'none';
        document.getElementById('trick-table-cards').style.display = 'none';
        document.getElementById('current-player-info').style.display = 'none';
        return;
    }

    if (index >= 0 && index < gameDataGlobal.tricks.length) {
        currentTrickIndex = index;
        currentPlayIndex = 0; // Reset play index when changing tricks
        currentTrickDisplay.textContent = `Trick ${currentTrickIndex + 1}/${gameDataGlobal.tricks.length}`;
        displayCurrentPlay();
    } else {
        // Handle invalid trick index (e.g., if prev/next goes out of bounds)
        console.warn("Invalid trick index requested.");
    }
}

function displayCurrentPlay() {
    const currentTrickContainer = document.getElementById('current-trick-container');
    const currentPlayDisplay = document.getElementById('current-play-display');
    const cardsOnTableDiv = document.getElementById('cards-on-table');
    const currentPlayerNameSpan = document.getElementById('current-player-name');
    const cardPlayedByCurrentPlayerDiv = document.getElementById('card-played-by-current-player');
    const currentPlayerHandDiv = document.getElementById('current-player-hand');
    const currentTrickDisplay = document.getElementById('current-trick-display');

    const currentTrick = gameDataGlobal.tricks[currentTrickIndex];

    if (!gameDataGlobal || !gameDataGlobal.tricks || gameDataGlobal.tricks.length === 0) {
        currentTrickDisplay.textContent = 'Trick 0/0';
        currentPlayDisplay.textContent = 'Play 0/0';
        cardsOnTableDiv.innerHTML = '';
        currentPlayerNameSpan.textContent = '';
        cardPlayedByCurrentPlayerDiv.innerHTML = '';
        currentPlayerHandDiv.innerHTML = '';
        return;
    }

    if (!currentTrick || currentPlayIndex >= currentTrick.cards_played.length) {
        currentPlayDisplay.textContent = 'Play 0/0';
        cardsOnTableDiv.innerHTML = '';
        currentPlayerNameSpan.textContent = '';
        cardPlayedByCurrentPlayerDiv.innerHTML = '';
        currentPlayerHandDiv.innerHTML = '';
        return;
    }

    const currentPlay = currentTrick.cards_played[currentPlayIndex];
    const currentPlayer = currentPlay.player;
    const cardPlayed = currentPlay.card;

    currentTrickDisplay.textContent = `Trick ${currentTrickIndex + 1}/${gameDataGlobal.tricks.length}`;
    currentPlayDisplay.textContent = `Play ${currentPlayIndex + 1}/${currentTrick.cards_played.length}`;

    // Display cards on table (cards played before the current play in this trick)
    cardsOnTableDiv.innerHTML = '';
    if (currentPlayIndex === 0) {
        cardsOnTableDiv.innerHTML = '<p>No cards played yet in this trick.</p>';
    } else {
        for (let i = 0; i < currentPlayIndex; i++) {
            const playedCard = currentTrick.cards_played[i];
            const playerCardPairDiv = document.createElement('div');
            playerCardPairDiv.innerHTML = `<strong>${playedCard.player}:</strong>`;
            playerCardPairDiv.appendChild(createCardElement(playedCard.card));
            cardsOnTableDiv.appendChild(playerCardPairDiv);
        }
    }

    // Display current player and card played
    currentPlayerNameSpan.textContent = currentPlayer;
    cardPlayedByCurrentPlayerDiv.innerHTML = '';
    cardPlayedByCurrentPlayerDiv.appendChild(createCardElement(cardPlayed));

    // Reconstruct and display player's hand
    const reconstructedHand = reconstructPlayerHand(currentPlayer, currentTrickIndex, currentPlayIndex);
    const sortedHand = sortCards(reconstructedHand);
    currentPlayerHandDiv.innerHTML = '';
    sortedHand.forEach(cardString => {
        currentPlayerHandDiv.appendChild(createCardElement(cardString));
    });
}

function prevTrick() {
    if (currentTrickIndex > 0) {
        displayTrick(currentTrickIndex - 1);
    }
}

function nextTrick() {
    if (gameDataGlobal && gameDataGlobal.tricks && currentTrickIndex < gameDataGlobal.tricks.length - 1) {
        displayTrick(currentTrickIndex + 1);
    }
}

function prevPlay() {
    if (currentPlayIndex > 0) {
        currentPlayIndex--;
        displayCurrentPlay();
    } else if (currentTrickIndex > 0) {
        // Go to the last play of the previous trick
        currentTrickIndex--;
        currentPlayIndex = gameDataGlobal.tricks[currentTrickIndex].cards_played.length - 1;
        displayCurrentPlay();
    }
}

function nextPlay() {
    const currentTrick = gameDataGlobal.tricks[currentTrickIndex];
    if (currentTrick && currentPlayIndex < currentTrick.cards_played.length - 1) {
        currentPlayIndex++;
        displayCurrentPlay();
    } else if (gameDataGlobal && gameDataGlobal.tricks && currentTrickIndex < gameDataGlobal.tricks.length - 1) {
        // Go to the first play of the next trick
        currentTrickIndex++;
        currentPlayIndex = 0;
        displayCurrentPlay();
    }
}

// Expose functions to the global scope for HTML to access
window.displayGame = displayGame;
window.prevTrick = prevTrick;
window.nextTrick = nextTrick;
window.prevPlay = prevPlay;
window.nextPlay = nextPlay;
function toggleGameInfo() {
    const gameInfoDiv = document.getElementById('game-info');
    gameInfoDiv.classList.toggle('hidden');
}
window.toggleGameInfo = toggleGameInfo;

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
        prevPlay();
    } else if (event.key === 'ArrowRight') {
        nextPlay();
    }
});