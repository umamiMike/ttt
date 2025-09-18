
		const client = mqtt.connect("ws://localhost:9001"); // Mosquitto WS listener

		client.on("connect", () => {
			client.subscribe("game/state", (err) => {
				if (!err) {
					msg = {action: "browser_connect", data: { }}
					client.publish("game/move", JSON.stringify(msg));
				}
			});
		});

		client.on("message", (topic, message) => {
			const response = JSON.parse(message.toString())
			if ("board_state" in response.data) {
				update_board(response.data.board_state)
			}
			switch (response.state) {
				case "joined":
					console.log(response)
					const plyrs = response.data.players;
					create_players(plyrs)
					break;
				case "full":
					console.log("game full")

					break;
				case "turn_taken":
					console.log("turn taken")
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

		const boardElement = document.getElementById('board');
		const statusElement = document.getElementById('status');
		const player_x = document.getElementById('player_x');
		const player_y = document.getElementById('player_y');
		const resetButton = document.getElementById('reset');
		const query_button = document.getElementById('query');


		let board = Array(9).fill('');
		let bs = Array(9).fill(0);
		let currentPlayer = 'X';
		let gameOver = false;

		function playerInfo(parent) {
			const name_prompt = document.createElement('input');
			name_prompt.placeholder = "Player Name"
			name_prompt.addEventListener("keypress", (e) => {
				if (e.key === "Enter") {
					const name = document.createElement('div')
					name.textContent = name_prompt.value
					join_game(name_prompt.value)
					// const par = name_prompt.parentElement
					// par.appendChild(name)
					// // name.textContent = name_prompt.value
					name_prompt.remove()
					// makeClickable()
				}
			});
			parent.appendChild(name_prompt)

		}
		function create_players(incoming_players) {
	
			incoming_players.forEach( (player) => {
				create_player(player)
			})

		}
		function create_player(player){

			const player_id = player.order === 1 ? "player_x" :  "player_o" 
			const player_ui = document.getElementById(player_id);
			const name_label = document.createElement('div');
			name_label.textContent = player_id
			const name_div = document.createElement('div');
			name_div.textContent = player.player
			player_ui.appendChild(name_label)
			player_ui.appendChild(name_div)
		}

		function join_game(name) {
			msg = {action: "join", data: {name: name}}
			client.publish("game/move", JSON.stringify(msg), {qos: 1});
		}
		function initBoard() {
			boardElement.innerHTML = '';
			board.forEach((cell, i) => {
				const cellDiv = document.createElement('div');
				cellDiv.classList.add('cell');
				cellDiv.textContent = cell;
				boardElement.appendChild(cellDiv);
			});
		}
		function makeClickable() {
			cells = document.querySelectorAll('.cell')
			cells.forEach((cell, i) => {
				cell.addEventListener('click', () => handleMove(i));
			});
		}

		function update_board(board_state) {
			cells = document.querySelectorAll('.cell')
			cells.forEach((cell, i) => {
				const val = board_state[i]
				const cell_content = val === 1 ? "X" : val === -1 ? "O" : ""
				cell.textContent = cell_content
			});
			makeClickable()
			}

		function handleMove(index) {
			console.log(index)
			const px = document.getElementById("player_x")
			const name = px.textContent
			msg = {action: "take_turn", data: {player: name, cell: index}}
			client.publish("game/move", JSON.stringify(msg), {qos: 1});

		}


		// resetButton.addEventListener('click', () => {
		// 	board = Array(9).fill('');
		// 	currentPlayer = 'X';
		// 	gameOver = false;
		// 	statusElement.textContent = `Next turn: ${currentPlayer}`;
		// 	renderBoard();
		// });

		// query_button.addEventListener('click', (e) => {
		// 	bn = board.map(item => {return item === "X" ? 1 : item === "O" ? -1 : 0})
		// 	client.publish("game/state", JSON.stringify(bn), {qos: 1});

		// });
		// Initial render
		initBoard();
		playerInfo(player_x);
		playerInfo(player_o);
		// statusElement.textContent = `Next turn: ${currentPlayer}`;
