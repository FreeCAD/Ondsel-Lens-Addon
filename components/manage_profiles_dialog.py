# SPDX-FileCopyrightText: 2025 Pieter Hijma <info@pieterhijma.net>
#
# SPDX-License-Identifier: LGPL-2.0-or-later

from PySide.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QMessageBox,
)
from PySide import QtCore

import FreeCADGui

import Utils

from models.profile import ProfileManager, ProfileListModel, Profile
from components.edit_profile_dialog import EditProfileDialog


logger = Utils.getLogger(__name__)


class ManageProfilesDialog(QDialog):

    def __init__(self, profile_manager: ProfileManager, parent=None):
        super().__init__(parent if parent else FreeCADGui.getMainWindow())

        self.ui = FreeCADGui.PySideUic.loadUi(
            Utils.mod_path + "/components/manage_profiles_widget.ui"
        )

        self.ui.setParent(self)
        self.setWindowTitle("Manage Profiles")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        self.profile_manager = profile_manager

        self.ui.buttonBox.clicked.connect(self.close)

        self.ui.createProfileButton.clicked.connect(self.create_profile)
        self.ui.editProfileButton.clicked.connect(self.edit_profile)
        self.ui.deleteProfileButton.clicked.connect(self.delete_profile)

        profile_list_model = ProfileListModel(profile_manager.get_profiles())
        self.ui.profilesView.setModel(profile_list_model)
        self.ui.profilesView.selectionModel().selectionChanged.connect(
            self.on_profile_selection_changed
        )
        self.on_profile_selection_changed()

    def on_profile_selection_changed(
        self,
        selected: QtCore.QItemSelection = None,
        deselected: QtCore.QItemSelection = None,
    ):
        def enable_buttons(enabled: bool):
            self.ui.editProfileButton.setEnabled(enabled)
            self.ui.deleteProfileButton.setEnabled(enabled)

        sm = self.ui.profilesView.selectionModel()
        if sm is None or not sm.hasSelection():
            enable_buttons(False)
        elif sm.hasSelection():
            enable_buttons(True)
        else:
            logger.error("Should not happen: Unexpected state for profile selection")
            enable_buttons(False)

    def create_profile(self):
        create_profile_dialog = EditProfileDialog(self.profile_manager, parent=self)
        if create_profile_dialog.exec() == QDialog.Accepted:
            new_profile = create_profile_dialog.get_profile()
            self.profile_manager.add_profile(new_profile)
            self.ui.profilesView.model().append_profile(new_profile)

    def edit_profile(self):
        profile: Profile = self.get_selected_profile()
        edit_profile_dialog = EditProfileDialog(
            self.profile_manager, profile=profile, parent=self
        )
        if edit_profile_dialog.exec() == QDialog.Accepted:
            updated_profile = edit_profile_dialog.get_profile()
            self.profile_manager.update_profile(updated_profile)

    def get_selected_profile(self) -> Profile:
        selected_indexes = self.ui.profilesView.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            profile = selected_index.data(ProfileListModel.ProfileRole)
            return profile
        return None

    def delete_profile(self):
        profile = self.get_selected_profile()
        if profile:
            confirm = QMessageBox.question(
                self,
                "Delete Profile",
                f"Are you sure you want to delete the profile '{profile.name}'?"
                f"\n\nThis will delete all local files.",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm == QMessageBox.Yes:
                self.profile_manager.remove_profile(profile)
                self.ui.profilesView.model().remove_profile(profile)
