# SPDX-FileCopyrightText: 2025 Pieter Hijma <info@pieterhijma.net>
#
# SPDX-License-Identifier: LGPL-2.0-or-later

from PySide.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
)

import FreeCADGui

import Utils


class LoginDialog(QDialog):
    def __init__(self, profile_name, lens_url, api_url, email, parent=None):
        super().__init__(parent if parent else FreeCADGui.getMainWindow())

        self.ui = FreeCADGui.PySideUic.loadUi(
            Utils.mod_path + "/components/login_widget.ui"
        )
        self.ui.setParent(self)
        self.setWindowTitle("Login")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        self.use_browser = False

        self.ui.profile_label.setText(profile_name)
        self.ui.lens_url_value.setText(lens_url)
        self.ui.api_url_value.setText(api_url)
        self.ui.email_value.setText(email)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Login")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        # Accounts created through an OAuth or OIDC provider have no local
        # password, so the password field alone cannot sign them in. Offer the
        # browser instead; it can use whichever provider the server offers.
        self.browser_button = self.ui.buttonBox.addButton(
            "Sign in with browser", QDialogButtonBox.ActionRole
        )
        self.browser_button.setToolTip(
            "Sign in through your browser. Use this for accounts created with "
            "GitHub, Google or another single sign-on provider."
        )
        self.browser_button.clicked.connect(self._choose_browser)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.ui.password_input.textChanged.connect(self.check_credentials)

    def check_credentials(self):
        password = self.ui.password_input.text()
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(password != "")

    def _choose_browser(self):
        self.use_browser = True
        self.accept()

    def wants_browser(self):
        return self.use_browser

    def get_password(self):
        return self.ui.password_input.text()
