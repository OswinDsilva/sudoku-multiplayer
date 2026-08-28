import { fetchBoard, makeMove, startGame } from "./api.js"

const gameboard = document.querySelector(".grid")
const number_selector = document.querySelector(".number-selector")

let selected_number
let selected_square
let resBoard

function displayGame() {
  for (let i = 1; i <= 9; i++) {
    for (let j = 1; j <= 9; j++) {
      let square = document.createElement("div")
      square.classList.add("square")
      square.id = `cell-${i}-${j}`
      if (resBoard.board[i - 1][j - 1] != 0)
        square.textContent = resBoard.board[i - 1][j - 1]
      square.addEventListener("click", async (event) => {
        const val = (i - 1) * 9 + j;
        if (selected_number === undefined) {
          console.log("Cannot fill with unselected")
        } else {
          let resMove = await makeMove(i - 1, j - 1, selected_number)
          console.log(resMove)
          if (resMove.ok) {
            square.textContent = selected_number
            const data = await resMove.json()
            if (data.completed === true) {
              alert("Completed!")
            }
          } else {
            const errorData = await resMove.json()
            alert(errorData.detail)
          }
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

let gameState = "not-started"
const startGameBtn = document.getElementById("startButton")
startGameBtn.addEventListener('click', async (event) => {
  if (gameState === "not-started") {
    resBoard = await startGame()
    gameState = "started"
    startGameBtn.style.display = 'none'
    displayGame()
  }
})
