Element tray
============

This project allows a better desktop integration for those who prefer to use [Element web](https://app.element.io/) instead of [Element desktop](https://element.io/download). Historically, Element desktop had some issues, especially on Linux / Wayland:

- [Screen sharing didn't work](https://github.com/element-hq/element-desktop/issues/1750).
- [Missing system tray icon](https://github.com/element-hq/element-web/issues/32907).

Or maybe you just want to avoid another Electron running besides your browser, to avoid additional memory / CPU usage.

So, this project allows you to use Element web in Chrome or Firefox, while showing a (rather simple) system tray icon, with a badge when there are unread messages, avoiding loosing new messages.

## How it works

This project is comprised of 2 parts: A Python app which displays the desktop icon and a browser extension which keeps monitoring the Element tab title. The Python app starts a small HTTP server which accepts a POST, and updates the icon. The extension keeps polling the tab title to send the POST request.

Besides, when clicking the icon, the extension is notified through the local HTTP server and focuses the Element tab. If no tab is found, a new one is created pointing to https://app.element.io. Notes:

- Clicking the icon works well on KDE Plasma, but in other environments, such as GNOME with the appindicator extension, clicking the icon will also show the menu (same as right-clicking), so this feature won't work;
- Extensions don't run on PWAs (installed web applications). So, if you have installed the Element web application, the extension won't run.

## Requirements

- Python 3
- PyQt6
- Qt 6.x
- Chrome or Firefox

## Installation

- The `main.py` can be executed directly. The tray click is handled by the extension polling the local HTTP server, so no browser is launched by the Python app itself. When you click the icon, the extension focuses the Element tab in the same window (whichever browser profile it lives in), so no profile configuration is needed.
- For the Chrome extension: navigate to [chrome://extensions/](chrome://extensions/), enable the 'Developer mode' switch in the top-right and click 'Load unpacked'. Select the 'chrome-extension' directory where you checked out this project. If you have Element open, you must reload it.
- For the Firefox extension:
  - **Persistent install**: Firefox stable only installs add-ons signed by Mozilla, so sign it yourself through AMO's unlisted channel. This is per-user: the signed `.xpi` is produced locally and gitignored, and anyone cloning the repo signs their own copy with their own AMO account. Steps:
    1. Create a free account at [addons.mozilla.org](https://addons.mozilla.org/) and generate an API key pair at [https://addons.mozilla.org/en-US/developers/addon/api/key/](https://addons.mozilla.org/en-US/developers/addon/api/key/). Store the API key and secret in your shell environment (e.g. `export WEB_EXT_API_KEY=...` and `export WEB_EXT_API_SECRET=...`).
    2. Install [web-ext](https://extensionworkshop.com/documentation/develop/getting-started-with-web-ext/) (`npm install --global web-ext`) and sign the unpacked extension (it has a `gecko.id` already): `cd firefox-extension && web-ext sign --channel unlisted`. This downloads a signed `element_tray_notifier-1.1.xpi` into `firefox-extension/web-ext-artifacts/`. Note that it signs the exact `version` in `manifest.json`; bump the version whenever you change the extension.
    3. Open the resulting `.xpi` in Firefox (File > Open File, or `firefox /path/to/file.xpi`). It installs permanently and survives restarts. The unlisted channel means it is never published on AMO — it's signed for your use only.
  - **Temporary install (dev/testing)**: navigate to [about:debugging#/runtime/this-firefox](about:debugging#/runtime/this-firefox), click 'Load Temporary Add-on' and select the `firefox-extension/manifest.json` file of this project. Note that temporary add-ons are removed when Firefox restarts; you'll need to reload it then.
  - In either case, if you have Element open, you must reload it.

Afterwards when getting new messages in Element, the tray icon should show a red badge. Once those messages are read, it should change back to the regular Element icon.

Tip: You can autostart the Python application by creating a file named `element-tray.desktop` in your `$HOME/.config/autostart` directory, with the following contents, remembering to replace `/home/user/git/element-tray` with the actual path where you've cloned this project:

```desktop
[Desktop Entry]
Exec=/path-to-git/element-tray/main.py
Name=element-tray
Type=Application
X-KDE-AutostartScript=true
```
