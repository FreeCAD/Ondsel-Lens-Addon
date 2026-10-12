# SPDX-FileCopyrightText: 2026 William Dunn <william.dunn@quasarke.net>
#
# SPDX-License-Identifier: LGPL-2.0-or-later

"""Loopback receiver for the browser sign-in flow.

The ondsel: URL scheme cannot carry the token on stock FreeCAD. Retrieving a
forwarded command line needs MainWindow.consumeReceivedScriptArgs(), which only
exists in Ondsel ES, and FreeCAD.ConfigGet("ScriptArgs") is empty when a running
instance receives the handoff rather than a fresh process.

A loopback HTTP receiver avoids both problems and is what RFC 8252 recommends
for native applications. The browser performs a top-level navigation to
127.0.0.1, so no mixed-content or private-network preflight applies.
"""

import http.server
import secrets
import threading
import urllib.parse

from PySide import QtCore

import Utils

logger = Utils.getLogger(__name__)

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title></head>
<body style="font-family:sans-serif;text-align:center;padding-top:4em">
<h2>{title}</h2><p>{body}</p></body></html>"""


def _page(title, body):
    return PAGE.format(title=title, body=body)


class BrowserLoginReceiver(QtCore.QObject):
    """Serves exactly one sign-in callback on a loopback port.

    Signals are emitted from the serving thread. Qt queues them to the
    receiver's thread, which keeps the login work on the GUI thread.
    """

    token_received = QtCore.Signal(str)
    failed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = secrets.token_urlsafe(24)
        self._httpd = None
        self._thread = None
        self._done = False

    def start(self):
        """Bind a loopback port and begin serving. Answers the port."""
        receiver = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass  # keep the stock stderr logging out of the Report view

            def do_GET(self):
                query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                token = (query.get("token") or [""])[0]
                state = (query.get("state") or [""])[0]

                if not state or not secrets.compare_digest(state, receiver.state):
                    # Guards against a stray or replayed callback landing here.
                    self.reply(
                        400,
                        "Sign-in could not be verified",
                        "This response did not match the request FreeCAD made.",
                    )
                    receiver.finish_with_error("the response did not match the request")
                    return

                if not token:
                    self.reply(
                        400,
                        "No token received",
                        "The browser did not return a sign-in token.",
                    )
                    receiver.finish_with_error("the browser returned no token")
                    return

                self.reply(
                    200,
                    "Signed in to FreeCAD",
                    "You can close this tab and return to FreeCAD.",
                )
                receiver.finish_with_token(token)

            def reply(self, code, title, body):
                data = _page(title, body).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self._httpd = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        port = self._httpd.server_address[1]
        self._thread = threading.Thread(
            target=self._httpd.serve_forever, name="ondsel-browser-login", daemon=True
        )
        self._thread.start()
        logger.debug(f"browser sign-in receiver listening on 127.0.0.1:{port}")
        return port

    def callback_url(self, port):
        return f"http://127.0.0.1:{port}/"

    def finish_with_token(self, token):
        if self._done:
            return
        self._done = True
        self.token_received.emit(token)
        self.stop()

    def finish_with_error(self, reason):
        if self._done:
            return
        self._done = True
        self.failed.emit(reason)
        self.stop()

    def time_out(self):
        self.finish_with_error("the browser did not respond in time")

    def stop(self):
        httpd, self._httpd = self._httpd, None
        if httpd is None:
            return
        # shutdown() must not run on the serving thread, so hand it to another.
        threading.Thread(target=self._close, args=(httpd,), daemon=True).start()

    @staticmethod
    def _close(httpd):
        try:
            httpd.shutdown()
        finally:
            httpd.server_close()
