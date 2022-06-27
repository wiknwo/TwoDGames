// Create board
let board = [
	['', '', ''],
	['', '', ''],
	['', '', '']
];

// Define game variables
let ai = 'X';
let human = 'O';
let currentPlayer = human;
let w;
let h;
let scores = {'X': 1, 'O': -1, 'tie': 0}; // Lookup table for minimax

// Functions
function setup() {
	// put setup code here
	createCanvas(400, 400);
	w = width / 3;
	h = height / 3;
	bestMove();
}

function nextTurn() {
	let index = floor(random(availableSpots.length));
	let spot = availableSpots.splice(index, 1)[0];
	let i = spot[0];
	let j = spot[1];
	board[i][j] = players[currentPlayer];
	currentPlayer = (currentPlayer + 1) % players.length;
}

function equals3(a, b, c) {
	return (a == b && b == c && a != '');
}

function checkWinner() {
	let winner = null;
	// Horizontals
	for (let i = 0; i < 3; i++) {
		if (equals3(board[i][0], board[i][1], board[i][2])) {
			winner = board[i][0];
		}
	}
	// Verticals
	for (let j = 0; j < 3; j++) {
		if (equals3(board[0][j], board[1][j], board[2][j])) {
			winner = board[0][j];
		}
	}
	// Diagonals
	if (equals3(board[0][0], board[1][1], board[2][2])) {
		winner = board[0][0];
	}
	if (equals3(board[0][2], board[1][1], board[2][0])) {
		winner = board[0][2];
	}

	// Counting open spots
	let openSpots = 0;
	for (let i = 0; i < 3; i++) {
		for (let j = 0; j < 3; j++) {
			if (board[i][j] == '') {
				openSpots++;
			}
		}
	}

	if (winner == null && openSpots == 0) {
		return 'tie';
	} else {
		return winner;
	}
}

function mousePressed() {
	if (currentPlayer == human) {
		// Human make turn
		let i = floor(mouseX / w);
		let j = floor(mouseY / h);
		// Check for valid turn
		if (board[i][j] == '') {
			board[i][j] = human;
			currentPlayer = ai;
			bestMove();
		}
	}
}

function bestMove() {
    // AI to make its turn
    let bestScore = -Infinity;
    let bestMove;
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            // Is the spot available?
            if (board[i][j] == '') {
                board[i][j] = ai;
                let score = minimax(board, 0, false);
                board[i][j] = ''; // Undo move
                if (score > bestScore) {
                    bestScore = score;
                    bestMove = {i, j}
                }
            }
        }
    }
    board[bestMove.i][bestMove.j] = ai;
    currentPlayer = human;
}

function minimax(board, depth, isMaximizing) {
    let result = checkWinner();
	if (result !== null) {
		return scores[result];
	}

	if (isMaximizing) {
		let bestScore = -Infinity;
		for (let i = 0; i < 3; i++) {
			for (let j = 0; j < 3; j++) {
				// Is the spot available
				if (board[i][j] == '') {
					board[i][j] = ai;
					let score = minimax(board, depth + 1, false);
					board[i][j] = '';
					bestScore = max(score, bestScore);
				}
			}
		}
		return bestScore;
	} else {
		let bestScore = Infinity;
		for (let i = 0; i < 3; i++) {
			for (let j = 0; j < 3; j++) {
				// Is the spot available
				if (board[i][j] == '') {
					board[i][j] = human;
					let score = minimax(board, depth + 1, true);
					board[i][j] = '';
					bestScore = min(score, bestScore);
				}
			}
		}
		return bestScore;
	}
}

function draw() {
	// put drawing code here
	background(200);

	// Drawing lines to separate X's and O's
	line(w, 0, w, height);
	line(w * 2, 0, w * 2, height);
	line(0, h, width, h);
	line(0, h * 2, width, h * 2);

	for (let j = 0; j < 3; j++) {
		for (i = 0; i < 3 ; i++) {
			let x = w * i + w / 2;
			let y = h * j + h / 2;
			let spot = board[i][j];
			textSize(32);
			strokeWeight(4);
			if (spot == human) {
				noFill();
				ellipse(x, y, w / 2);
			} else if (spot == ai) {
				let xradius = w / 4;
				line(x - xradius, y - xradius, x + xradius, y + xradius);
				line(x + xradius, y - xradius, x - xradius, y + xradius); 
			}
		}
	}
	let result = checkWinner();
	if (result != null) {
		noLoop();
		createP(result).style('color', '#000').style('font-size', '32pt').position(0, 450);
	}
	//nextTurn();
}
