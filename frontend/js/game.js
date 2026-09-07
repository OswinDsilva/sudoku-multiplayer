import { makeMove, startGame } from "./api.js"

const ws_url = window.location.origin.replace(/^http/, "ws")
console.log(ws_url)

const urlParams = new URLSearchParams(window.location.search)
const room_id = urlParams.get('id')
const socket = new WebSocket(`${ws_url}/api/room/${room_id}`)
console.log(room_id)


const gameboard = document.querySelector(".grid")
const number_selector = document.querySelector(".number-selector")

let selected_number
let selected_square
let resBoard
let gameState = "not-started"
const startGameBtn = document.getElementById("startButton")

socket.addEventListener("open", () => {
  socket.send(JSON.stringify({
    type: "retrieve_state"
  }))
})

socket.addEventListener("message", (event) => {
  const parsedData = JSON.parse(event.data)
  gameState = parsedData.body.gameState
  if (parsedData.type === "update_board") {
    resBoard = {
      "board": parsedData.body.board
    }

    console.log(resBoard)
    if (gameState === "started") {
      startGameBtn.style.display = 'none'
      displayGame()
    }
  }
})

function displayGame() {
  gameboard.innerHTML = ""
  for (let i = 1; i <= 9; i++) {
    for (let j = 1; j <= 9; j++) {
      let square = document.createElement("div")
      square.classList.add("square")
      square.id = `cell-${i}-${j}`
      if (resBoard.board[i - 1][j - 1] != 0)
        square.textContent = resBoard.board[i - 1][j - 1]

      square.addEventListener("click", (event) => {
        if (selected_number === undefined) {
          console.log("Cannot fill with unselected")
        } else {
          const message = {
            "type": "fill_cell",
            "body": {
              "row": i - 1,
              "col": j - 1,
              "val": selected_number
            }
          }
          socket.send(JSON.stringify(message))
        }
      })

      if (i % 3 == 0) {
        square.style.setProperty('border-bottom', '2px solid black');
      }
      if ((i - 1) % 3 == 0) {
        square.style.setProperty('border-top', '2px solid black');
      }
      if (j % 3 == 0) {
        square.style.setProperty('border-right', '2px solid black');
      }
      if ((j - 1) % 3 == 0) {
        square.style.setProperty('border-left', '2px solid black');
      }
      gameboard.append(square)
    }
  }

  number_selector.innerHTML = ""
  for (let i = 1; i <= 9; i++) {
    let square = document.createElement("div")
    square.classList.add("square")
    square.id = `number-${i}`
    square.style.setProperty('border', '2px solid black')
    square.textContent = i
    square.addEventListener("click", function () {
      if (selected_number !== undefined) {
        selected_square = document.getElementById(`number-${selected_number}`)
        selected_square.style.setProperty('background-color', 'white')
      }

      selected_number = i
      square.style.setProperty('background-color', 'skyblue')
    })

    number_selector.append(square)
  }
}

startGameBtn.addEventListener('click', async (event) => {
  if (gameState === "not-started") {
    const message = {
      "type": "start_game"
    }
    socket.send(JSON.stringify(message))
  }
})
