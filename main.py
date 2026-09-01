#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QSystemTrayIcon
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DEFAULT = os.path.join(SCRIPT_DIR, "icon.png")
ICON_ALERT = os.path.join(SCRIPT_DIR, "icon_alert.png")
BROWSER = os.getenv('BROWSER', 'google-chrome-stable')
CHROME_PROFILE = os.getenv('CHROME_PROFILE')
FIREFOX_PROFILE = os.getenv('FIREFOX_PROFILE')
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
            cmd = [BROWSER]
            if BROWSER == 'google-chrome-stable':
                if CHROME_PROFILE:
                    cmd.append(f"--profile-directory={CHROME_PROFILE}")
            else:
                if FIREFOX_PROFILE:
                    cmd += ["-P", FIREFOX_PROFILE]
            cmd.append(f"http://localhost:{PORT}/open")
            subprocess.Popen(cmd, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def quit(self):
        self.setVisible(False)
        QtWidgets.QApplication.quit()

class RequestHandler(BaseHTTPRequestHandler):
    tray_ref = None  # static reference to tray icon

    def do_POST(self):
        """Handle POST requests (to update the tray icon)"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode()
            else:
                post_data = ""

            if post_data == "alert":
                RequestHandler.tray_ref.alert()
            elif post_data == "reset":
                RequestHandler.tray_ref.reset()

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', '2')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(b'OK')
        except (BrokenPipeError, ConnectionResetError):
            # Client disconnected, ignore the error
            pass
        except Exception as e:
            # Log other errors but don't crash
            print(f"Error handling POST request: {e}")

    def do_GET(self):
        """Handle GET requests (the browser opens /open on tray click; the extension intercepts it)"""
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', '2')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(b'OK')
        except (BrokenPipeError, ConnectionResetError):
            # Client disconnected, ignore the error
            pass
        except Exception as e:
            # Log other errors but don't crash
            print(f"Error handling GET request: {e}")

    def do_OPTIONS(self):
        """Handle OPTIONS requests (for CORS preflight)"""
        try:
            self.send_response(200)
            self.send_header('Allow', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Origin', 'https://app.element.io')
            self.send_header('Connection', 'close')
            self.end_headers()
        except (BrokenPipeError, ConnectionResetError):
            pass

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
