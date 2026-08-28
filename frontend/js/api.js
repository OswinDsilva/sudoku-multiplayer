const backend_url = "http://localhost:8000"

export async function startGame() {
  const url = backend_url + "/boards/start"
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Length': '0' // Best practice for empty POST requests
      }
    })
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }

    const result = await response.json()
    return result
  } catch (error) {
    console.error(error.message)
  }
}

export async function fetchBoard() {
  const url = backend_url + "/boards/board";
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }

    const result = await response.json()
    return result
  } catch (error) {
    console.error(error.message)
  }
}

export async function makeMove(row, col, val) {
  const url = backend_url + "/boards/fill";
  const payload = {
    row: row,
    col: col,
    val: val
  }
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload)
    })

    return response
  } catch (error) {
    console.error(error.message)
  }
}
