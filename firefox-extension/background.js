const TRIGGER = "http://localhost:45678/open";

function handle(url, tabId) {
  if (url && url.includes(TRIGGER)) {
    chrome.tabs.remove(tabId);
    chrome.tabs.query({ url: "https://app.element.io/*" }, (tabs) => {
      if (tabs.length > 0) {
        chrome.tabs.update(tabs[0].id, { active: true });
      } else {
        chrome.tabs.create({ url: "https://app.element.io" });
      }
    });
  }
}

chrome.tabs.onCreated.addListener((tab) => {
  handle(tab.pendingUrl || tab.url, tab.id);
});
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  handle(changeInfo.url || (tab && tab.url), tabId);
});