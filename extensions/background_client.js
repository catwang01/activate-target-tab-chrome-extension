let socket;

// Establish WebSocket connection
function connectWebSocket() {
  socket = new WebSocket("ws://localhost:8080"); // Replace with your WebSocket server URL

  socket.onopen = function (event) {
    console.log("WebSocket connection established");
  };

  socket.onmessage = function (event) {
    const message = JSON.parse(event.data);
    console.log("Recevied data: ");
    console.log(message);
    if (message.action === "activateTab") {
      const tabUrl = message.tabUrl;
      // var tabs = await chrome.tabs.query({}, tab => tab.url === tabUrl)
      chrome.tabs.query({}, (tabs) => {
        console.log({ tabs });
        const filtered = tabs.filter((tab) => tab.url === tabUrl);
        console.log(`${filtered.length} tabs are found!`);
        socket.send(`${filtered.length} tabs are found!`);
        console.log(filtered);
        const target = filtered[0];
        chrome.tabs.update(target.id, { active: true }, () => {
          socket.send("tab is activated!");
          chrome.tabs.sendMessage(target.id, { action: "search_notes" });
        });
      });
    }
  };

  socket.onclose = function (event) {
    console.log("WebSocket connection closed");
    // Attempt to reconnect after a delay (optional)
    setTimeout(connectWebSocket, 5000);
  };
}

// Connect WebSocket on extension startup
connectWebSocket();

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  console.log('Message received in background.js', message);
});
