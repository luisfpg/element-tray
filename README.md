Element tray
============

[Element desktop](https://element.io/download) is great, but so far in Linux with Wayland, there has been problems with screen sharing with the underlying Electron platform.

As a workaround, it is possible to use the [Element web](https://app.element.io/) in Chrome, where screen sharing works flawlessly. However, when doing so, the system tray icon to indicate new messages is lost.

This project attempts to bridge this gap, by having a (rather simple) tray icon. It changes the icon to a red badge when there are unread messages in the Element web tab.

## How it works

This project is comprised of 2 parts: A Python app which displays the desktop icon and a Chrome extension which keeps monitoring the Element tab title. The Python app starts a small HTTP server which accepts a POST, and updates the icon. The chrome extension keeps polling the tab title to send the POST request.

Besides, when clicking the icon it opens a special localhost URL in the Chrome browser that gets intercepted by the extension. The new tab is closed and the current Element tab is focused. If no tab is found, a new one is created pointing to https://app.element.io. Notes:

- Clicking the icon works well on KDE Plasma, but in other environments, such as GNOME with the appindicator extension, clicking the icon will also show the menu (same as right-clicking), so this feature won't work;
- If you have multiple Chrome profiles, you need to set the `CHROME_PROFILE` environment variable. More on this below;
- Chrome extensions don't run on PWAs (installed web applications). So, if you have installed the Element web application, the chrome extension won't run.

## Requirements

- Python 3
- PyQt6
- Qt 6.x
- Google Chrome

## Installation

- The `main.py` can be executed directly. Note that if you have multiple Chrome profiles, you need the `CHROME_PROFILE` environment variable pointing to your profile name. Otherwise it will open in the last used Chrome window, which could be of another profile. To see the internal profile identifier, open Chrome (with the same profile as the Element app) and navigate to [chrome://version](chrome://version). You will see something like 'Profile path'. Take note of the last part of the path (which might contain spaces). Example: `/home/user/.config/google-chrome/Profile 1`. In this case, set the environment variable `CHROME_PROFILE="Profile 1"`;
- For the Chrome extension, in Chrome, navigate to [chrome://extensions/](chrome://extensions/), enable the 'Developer mode' switch in the top-right and click 'Load unpacked'. Select the 'chrome-extension' directory where you checked out this project. If you have Element open, you must reload it.

Afterwards when getting new messages in Element, the tray icon should show a red badge. Once those messages are read, it should change back to the regular Element icon.

Tip: You can autostart the Python application by creating a file named `element-tray.desktop` in your `$HOME/.config/autostart` directory, with the following contents, remembering to replace `/home/user/git/element-tray` with the actual path where you've cloned this project:

```desktop
[Desktop Entry]
Exec=/home/user/git/element-tray/main.py
Name=element-tray
Type=Application
X-KDE-AutostartScript=true
```
