// Content script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  console.log('Message received in content script:', message);
  if (message.action === "search_notes")
  {
    var [ searchButton ] = document.getElementsByClassName("bm-search");
    console.log( { searchButton });
    searchButton.click();
    sendResponse({farewell: "goodbye"});
  }
});

