# SPDX-FileCopyrightText: 2025 Pieter Hijma <info@pieterhijma.net>
#
# SPDX-License-Identifier: LGPL-2.0-or-later

import re

from PySide.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QLabel,
)

import FreeCADGui

import Utils

from models.profile import Profile, ProfileManager

logger = Utils.getLogger(__name__)


class EditProfileDialog(QDialog):

    def __init__(
        self, profile_manager: ProfileManager, profile: Profile = None, parent=None
    ):
        super().__init__(parent if parent else FreeCADGui.getMainWindow())

        self.ui = FreeCADGui.PySideUic.loadUi(
            Utils.mod_path + "/components/edit_profile_widget.ui"
        )

        self.ui.setParent(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        self.profile_manager = profile_manager
        self.profile = profile

        if profile is None:
            self.setWindowTitle("Create Profile")
            self.name_profile_input = QLineEdit()
            self.name_profile_input.setPlaceholderText(
                "alphanumeric characters, underscores, or hyphens"
            )
            self.ui.formLayout.setWidget(
                0, QFormLayout.FieldRole, self.name_profile_input
            )
            self.name_profile_input.setFocus()
            self.name_profile_input.textChanged.connect(self.validate_input)
        else:
            self.setWindowTitle("Edit Profile")
            self.ui.formLayout.setWidget(0, QFormLayout.FieldRole, QLabel(profile.name))
            self.ui.lens_url_input.setText(profile.lens_url)
            self.ui.api_url_input.setText(profile.api_url)
            self.ui.email_input.setText(profile.email)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.ui.email_input.textChanged.connect(self.validate_input)

    def validate_input(self):
        valid_input = True
        if self.profile is None:
            valid_input = self.validate_profile_name(self.name_profile_input.text())

        email = self.ui.email_input.text()
        valid_input = valid_input and self.validate_email(email)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid_input)

    def validate_profile_name(self, profile_name) -> bool:
        profile_name = profile_name.strip()

        return profile_name != "" and ProfileManager.is_valid_profile_name(profile_name)

    def validate_email(self, email) -> bool:
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    def get_text_input_field(self, input_field):
        return (
            input_field.placeholderText()
            if input_field.text() == ""
            else input_field.text()
        )

    def get_profile(self):
        if self.profile is None:
            name_profile = self.name_profile_input.text()
        else:
            name_profile = self.profile.name

        lens_url = self.get_text_input_field(self.ui.lens_url_input)
        api_url = self.get_text_input_field(self.ui.api_url_input)
        email = self.ui.email_input.text()

        return Profile(
            name=name_profile, lens_url=lens_url, api_url=api_url, email=email
        )
