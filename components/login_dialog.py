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

        self.ui.profile_label.setText(profile_name)
        self.ui.lens_url_value.setText(lens_url)
        self.ui.api_url_value.setText(api_url)
        self.ui.email_value.setText(email)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Login")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.ui.password_input.textChanged.connect(self.check_credentials)

    def check_credentials(self):
        password = self.ui.password_input.text()
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(password != "")

    def get_password(self):
        return self.ui.password_input.text()
