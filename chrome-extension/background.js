chrome.tabs.onCreated.addListener((tab) => {
  if (tab.pendingUrl && tab.pendingUrl.includes("http://localhost:45678/open")) {
    chrome.tabs.query({ url: "https://app.element.io/*" }, (tabs) => {
      if (tabs.length > 0) {
        chrome.tabs.update(tabs[0].id, { active: true });
      } else {
        chrome.tabs.create({ url: "https://app.element.io" });
      }
    });
    chrome.tabs.remove(tab.id);
  }
});
