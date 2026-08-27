const gameboard = document.querySelector(".grid")
const number_selector = document.querySelector(".number-selector")

for (let i = 1; i <= 9; i++){
  for (let j = 1; j <= 9; j++) {
    let square = document.createElement("div")
    square.classList.add("square")
    if (i % 3 == 0) {
      square.style.setProperty('border-bottom', '2px solid black');
    }
    if ((i - 1) % 3 == 0) {
      square.style.setProperty('border-top', '2px solid black');
    }
    if (j % 3 == 0) {
      square.style.setProperty('border-right', '2px solid black');
    }
    if ((j-1) % 3 == 0) {
      square.style.setProperty('border-left', '2px solid black');
    }
    gameboard.append(square)
  }
}

for (let i = 1; i <= 9; i++){
  let square = document.createElement("div")
  square.classList.add("square")
  square.style.setProperty('border', '2px solid black')
  number_selector.append(square)
}
