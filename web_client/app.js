const client = mqtt.connect("ws://localhost:9001"); // Mosquitto WS listener
client.on("connect", () => {
    client.subscribe("game/state", (err) => {
        if (!err) {
            msg = { action: "browser_connect", data: { msg: "connecto" } }
            client.publish("game/move", JSON.stringify(msg));
        }
    });
});

client.on("message", (topic, message) => {
    const response = JSON.parse(message.toString())
    if ("board_state" in response.data) {
        update_board(response.data.board_state)
    }
    if ("player" in response.data) {
        console.log(response)
        updatePlayers(response.data.player)
    }
    if ("players" in response.data) {
        create_players(response.data.players)
    }
    if ("starting_player" in response.data) {
        startPlayer(response.data.starting_player.player)
    }
    switch (response.state) {
        case "connected":
            console.log(response)
            if (response.data.players.length < 2 && !joined) {
                playerForm(infoElement)
            }
            status_update("hitting reset will clear the board and remove all players")
            //create_players(plyrs)
            break;
        case "joined":
            console.log(response)
            joined = true
            if (response.data.players.length == 1) {
                first = true
            }
            status_update("")
            break;
        case "started":
            console.log("started")
            console.log(response.data)
            break;
        case "full":
            remove_form()
            console.log("game full")
            status_update("there can ony be 2 players")
            break;
        case "turn_taken":
            status_update("")
            break;
        case "game_won":
            console.log(response.data)
            winner = response.data.player
            setWinner(winner)
            break;
        case "reset":
            console.log("reset")
            update_board(response.data.board_state)
            joined = false
            playerForm(infoElement)
            console.log(response.data)
            first = false
            break;
        case "no_turn":
            status_update("the player needs to go first")
            break;
        default:
            console.log("unhandled")
            console.log(response);
    }

});

client.on("error", (topic, message) => {
    console.log(topic, message.toString());
});

const infoElement = document.getElementById("info")
const boardElement = document.getElementById('board');
const statusElement = document.getElementById('status');
const players_ui = document.getElementById('players');
const resetButton = document.getElementById('reset');
const query_button = document.getElementById('query');
const reset_button = document.getElementById('reset');

let board = Array(9).fill('');
let bs = Array(9).fill(0);

// hacky... this is just for the current player session
let player_name = ""
let joined = false
let first = false
let winner = ""

function remove_form() {
    infoElement.replaceChildren()
}

function playerForm(parent) {
    remove_form()
    if (joined == true) return
    const name_prompt = document.createElement('input');
    name_prompt.id = "player_input"
    name_prompt.placeholder = `Join the game`
    name_prompt.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            const name = document.createElement('div')
            name.textContent = name_prompt.value
            player_name = name_prompt.value
            //need to delete the prompt from the other player
            join_game(name_prompt.value)
            name_prompt.remove()
        }
    });
    parent.appendChild(name_prompt)
}

function create_players(incoming_players) {
    players_ui.replaceChildren()
    incoming_players.forEach((player) => {
        create_player(player)
    })

}

function create_player(player) {
    const player_ui = document.createElement('div');
    player_ui.classList.add('player')
    player_ui.id = player.player
    const name_label = document.createElement('p');
    const name_div = document.createElement('p');
    const ord = player.order == 1 ? "X" : "O"
    name_label.textContent = `${ord} player: `
    name_div.id = player.player
    name_div.textContent = player.player
    player_ui.appendChild(name_label)
    player_ui.appendChild(name_div)
    players_ui.appendChild(player_ui)

}

function startPlayer(player) {
    for (const child of players_ui.children) {
        if (child.lastChild.id == player) {
            child.classList.add('active');
        }

    }
}

function setWinner(player) {
    for (const child of players_ui.children) {
        if (child.lastChild.id == player) {
            child.classList.add('winner');
        }
        else {
            child.classList.remove('active');

        }

    }
}
function updatePlayers(player) {
    for (const child of players_ui.children) {
        if (child.lastChild.id == player) {
            child.classList.remove('active');
        }
        else {
            child.classList.add('active');
        }

    }
}

function join_game(name) {

    msg = { action: "join", data: { name: name } }
    client.publish("game/move", JSON.stringify(msg), { qos: 0 });
}
function initBoard() {
    boardElement.innerHTML = '';
    board.forEach((cell, i) => {
        const cellDiv = document.createElement('div');
        cellDiv.classList.add('cell');
        cellDiv.textContent = cell;
        boardElement.appendChild(cellDiv);
        cellDiv.addEventListener('click', () => handleMove(i));
    });
}

function update_board(board_state) {
    cells = document.querySelectorAll('.cell')
    cells.forEach((cell, i) => {
        const val = board_state[i]
        const cell_content = val === 1 ? "X" : val === -1 ? "O" : ""
        cell.textContent = cell_content;
    });
}

function handleMove(index) {
    msg = { action: "take_turn", data: { player: player_name, cell: index } }
    client.publish("game/move", JSON.stringify(msg), { qos: 0 });
}

reset_button.addEventListener('click', () => reset_game());
function reset_game() {

    msg = { action: "reset", data: {} }
    client.publish("game/move", JSON.stringify(msg), { qos: 0 });
}

function status_update(msg) {
    statusElement.replaceChildren()
    statusElement.textContent = msg
}

initBoard();
