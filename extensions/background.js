
// chrome.runtime.onConnectExternal.addListener(function (port) {
//   if (port.name === "websocket") {
//     connectedClients.add(port);
//
//     port.onDisconnect.addListener(function () {
//       connectedClients.delete(port);
//     });
//
//     port.onMessage.addListener(function (message) {
//       if (message.action === "activateTab") {
//         const tabId = message.tabId;
//         chrome.tabs.update(tabId, { active: true });
//       }
//     });
//   }
// });

// chrome.runtime.onMessageExternal.addListener(function (request, sender, sendResponse) {
//   if (request.action === "register") {
//     if (!server) {
//       server = new WebSocketServer();
//     }
//     sendResponse({ success: true });
//   }
// });

class WebSocketServer {
  constructor() {
    this.server = new WebSocket("ws://localhost:8080"); // Replace with your server's WebSocket URL
    this.server.onopen = this.handleOpen.bind(this);
    this.server.onmessage = this.handleMessage.bind(this);
    this.server.onclose = this.handleClose.bind(this);
  }

  handleOpen(event) {
    console.log("WebSocket server connection established");
  }

  handleMessage(event) {
    const message = JSON.parse(event.data);
    this.sendToConnectedClients(message);
  }

  handleClose(event) {
    console.log("WebSocket server connection closed");
    this.server = null;
  }

  sendToConnectedClients(message) {
    connectedClients.forEach(function (client) {
      client.postMessage(message);
    });
  }
}

let server = new WebSocketServer();
let connectedClients = new Set();
