let lastTitle = null;
let lastAction = null;

function notifyTray(action) {
  fetch("http://127.0.0.1:45678", {
    method: "POST",
    body: action,
    mode: "no-cors"
  }).catch(() => {});
}

function handleTitleChange(newTitle) {
  if (newTitle !== lastTitle) {
    const action = newTitle.includes("Element [") ? "alert" : "reset";
    if (lastAction !== action) {
      console.log(`Title changed to: ${newTitle}, Action: ${action}`);
      notifyTray(action);
      lastAction = action;
    }
    lastTitle = newTitle;
  }
}

setInterval(() => {
  handleTitleChange(document.title);
}, 1000);
