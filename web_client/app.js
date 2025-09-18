
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
			console.log(response);
			if ("board_state" in response.data) {
				update_board(response.data.board_state)
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

		function playerInfo() {
			const name = "mike"
			const name_prompt = document.createElement('input');
			name_prompt.placeholder = "Player Name"
			name_prompt.addEventListener("keypress", (e) => {
				if (e.key === "Enter") {
					const name = document.createElement('div')
					name.textContent = name_prompt.value
					const par = name_prompt.parentElement
					par.appendChild(name)
					// name.textContent = name_prompt.value
					name_prompt.remove()
					join_game(name.textContent)
					makeClickable()
				}
			});
			player_x.appendChild(name_prompt)

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
		playerInfo();
		statusElement.textContent = `Next turn: ${currentPlayer}`;
