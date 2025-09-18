		const client = mqtt.connect("ws://localhost:9001"); // Mosquitto WS listener
		client.on("connect", () => {
			client.subscribe("game/state", (err) => {
				if (!err) {
					msg = {action: "browser_connect", data: { msg: "connecto" }}
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
				updatePlayer(response.data.player)
			}
			if ("players" in response.data) {
				create_players(response.data.players)
			}
			switch (response.state) {
				case "connected":
					console.log("connn")
					console.log(response)
					if (response.data.players.length < 2 && !joined ){
						playerForm(infoElement)
					}
					//create_players(plyrs)
					break;
				case "joined":
					console.log(response)
					joined = true
					break;
				case "started":
					console.log("started")
					// console.log(response.data)
					break;
				case "started":
					console.log("started")
					// console.log(response.data)
					break;
				case "full":
					remove_form()
					console.log("game full")
					break;
				case "turn_taken":
					console.log("turn taken")
					console.log(response.data)
					break;
				case "game_won":
					console.log("game won")
					console.log(response.data)
					break;
				case "reset":
					console.log("reset")
					update_board(response.data.board_state)
					joined = false
					playerForm(infoElement)
					console.log(response.data)
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
			incoming_players.forEach( (player) => {
				create_player(player)
			})

		}
		
		function create_player(player){
			const player_ui = document.createElement('div');
			player_ui.classList.add('player')
			player_ui.id = player
			const name_label = document.createElement('p');
			const name_div = document.createElement('p');
			name_label.textContent = "player: "
			name_div.id = player.player
			name_div.textContent = player.player
			player_ui.appendChild(name_label)
			player_ui.appendChild(name_div)
			players_ui.appendChild(player_ui)	

		}

		function join_game(name) {

			msg = {action: "join", data: {name: name}}
			client.publish("game/move", JSON.stringify(msg), {qos: 0});
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

		function updatePlayer(player) {
			const players_ui = document.getElementById('players');
			for (const child of players_ui.children) {
				if (child.lastChild.id == player) {
					child.classList.remove('active');
				}
				else {
					child.classList.add('active');
				}

			}
		}

		function handleMove(index) {
			msg = {action: "take_turn", data: {player: player_name, cell: index}}
			client.publish("game/move", JSON.stringify(msg), {qos: 0});
		}

		reset_button.addEventListener('click', () => reset_game());
 		function reset_game(){

			msg = {action: "reset", data: { } }
			client.publish("game/move", JSON.stringify(msg), {qos: 0});
		}


		initBoard();
		// initPlayer(player_x);
		// initPlayer(player_o);
		// statusElement.textContent = `Next turn: ${currentPlayer}`;
