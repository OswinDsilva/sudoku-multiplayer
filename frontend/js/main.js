import { createRoom, orig_url } from "./api.js"

const createRoomBtn = document.getElementById("createRoomButton")
createRoomBtn.addEventListener('click', async (event) => {
  const data = await createRoom(3)
  window.location.href = `${orig_url}/game.html?id=${data.room_id}`
})
