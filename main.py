#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QSystemTrayIcon
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DEFAULT = os.path.join(SCRIPT_DIR, "icon.png")
ICON_ALERT = os.path.join(SCRIPT_DIR, "icon_alert.png")
CHROME_PROFILE = os.getenv('CHROME_PROFILE')
PORT = 45678

class NotifierTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.menu = QtWidgets.QMenu()

        self.icon_default = QtGui.QIcon(ICON_DEFAULT)
        self.icon_alert = QtGui.QIcon(ICON_ALERT)

        self.setIcon(self.icon_default)

        self.activated.connect(self.on_tray_icon_click)

        quit_action = self.menu.addAction("Quit")
        quit_action.triggered.connect(self.quit)

        self.setContextMenu(self.menu)
        self.setVisible(True)

    def alert(self):
        self.setIcon(self.icon_alert)

    def reset(self):
        self.setIcon(self.icon_default)

    def on_tray_icon_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            profile_part = f"--profile-directory=\"{CHROME_PROFILE}\"" if CHROME_PROFILE else ""
            os.system(f"google-chrome-stable {profile_part} http://localhost:{PORT}/open")

    def quit(self):
        self.setVisible(False)
        QtWidgets.QApplication.quit()

class RequestHandler(BaseHTTPRequestHandler):
    tray_ref = None  # static reference to tray icon

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()

        if post_data == "alert":
            RequestHandler.tray_ref.alert()
        elif post_data == "reset":
            RequestHandler.tray_ref.reset()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, format, *args):
        return  # suppress logging

def start_server():
    server = HTTPServer(('127.0.0.1', PORT), RequestHandler)
    server.serve_forever()

def main():
    app = QtWidgets.QApplication(sys.argv)

    tray = NotifierTray(app)
    RequestHandler.tray_ref = tray

    # start HTTP server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
