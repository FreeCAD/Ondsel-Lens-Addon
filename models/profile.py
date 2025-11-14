# SPDX-FileCopyrightText: 2025 Pieter Hijma <info@pieterhijma.net>
#
# SPDX-License-Identifier: LGPL-2.0-or-later

import os
import shutil
from typing import List, Dict, Any
import json
from pathlib import Path

from dataclasses import dataclass, asdict, field

from PySide.QtCore import QAbstractListModel, QModelIndex, Qt

import Utils

from DataModels import CACHE_PATH

PROFILE_FILE_NAME = "profile.json"

logger = Utils.getLogger(__name__)


@dataclass(order=True)
class Profile:
    name: str
    lens_url: str
    api_url: str
    email: str
    access_token: str = ""
    logged_in: bool = True
    user: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(cls, json_data):
        return Utils.import_json_forgiving_of_extra_fields(cls, json_data)


class ProfileManager:
    def __init__(self):
        self.profiles = self.find_profiles()
        self.current_profile = None

    def find_profiles(self) -> List[Profile]:
        profiles = []
        cache_path = Utils.ensure_dir_exists(CACHE_PATH)
        for entry in os.listdir(cache_path):
            entry_path = os.path.join(cache_path, entry)
            if self.is_profile_dir(entry_path):
                profile_file = os.path.join(entry_path, PROFILE_FILE_NAME)
                with open(profile_file, "r") as f:
                    profile_data = json.load(f)
                    profile = Profile.from_json(profile_data)
                    profiles.append(profile)
        return profiles

    def is_profile_dir(self, path: str) -> bool:
        base = Path(os.path.normcase(os.path.abspath(CACHE_PATH)))
        p = Path(os.path.normcase(os.path.abspath(path)))

        try:
            if not p.is_relative_to(base):
                return False
        except ValueError:
            # This can happen if there are different drives on Windows
            return False

        if p.parent != base:
            return False

        return p.is_dir() and (p / PROFILE_FILE_NAME).is_file()

    @staticmethod
    def is_valid_profile_name(name: str) -> bool:
        return all(c.isalnum() or c in ("_", "-") for c in name) and not os.path.exists(
            os.path.join(CACHE_PATH, name)
        )

    def add_profile(self, profile: Profile):
        self.profiles.append(profile)

    def delete_profile_files(self, profile: Profile):
        cache_root = Path(CACHE_PATH).resolve()
        profile_dir = cache_root / profile.name

        try:
            profile_dir_resolved = profile_dir.resolve()
        except FileNotFoundError:
            logger.error(
                f"Profile directory '{profile_dir}' does not exist. Skipping deletion."
            )
            return

        try:
            shutil.rmtree(profile_dir_resolved)
        except Exception as e:
            logger.error(
                f"Failed to remove profile directory '{profile_dir_resolved}': {e}"
            )

    def remove_profile(self, profile: Profile):
        self.delete_profile_files(profile)
        self.profiles.remove(profile)
        if self.current_profile == profile:
            self.current_profile = None

    def update_profile(self, profile: Profile):
        if profile != self.current_profile:
            logger.error(
                "Updating a profile that is not the current profile. This may lead to inconsistencies."
            )
        profile_dir = os.path.join(CACHE_PATH, profile.name)
        Utils.ensure_dir_exists(profile_dir)
        profile_file = os.path.join(profile_dir, PROFILE_FILE_NAME)
        with open(profile_file, "w") as f:
            json.dump(asdict(profile), f, indent=2)

    def get_profiles(self):
        return self.profiles

    def get_profile_by_name(self, profile_name: str):
        for profile in self.profiles:
            if profile.name == profile_name:
                return profile
        return None

    def set_current_profile(self, profile_name: str):
        self.current_profile = self.get_profile_by_name(profile_name)

    def get_current_profile(self):
        return self.current_profile

    def set_current_profile_logged_in(self, logged_in: bool):
        if self.current_profile:
            self.current_profile.logged_in = logged_in
            self.update_profile(self.current_profile)


class ProfileListModel(QAbstractListModel):

    ProfileRole = Qt.UserRole + 1

    def __init__(self, profiles=None, parent=None):
        super().__init__(parent)
        self.profiles = list(profiles or [])

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self.profiles[index.row()].name
        elif role == self.ProfileRole:
            return self.profiles[index.row()]
        return None

    def roleNames(self):
        roles = super().roleNames()
        roles[self.ProfileRole] = b"profile"
        return roles

    def rowCount(self, parent=QModelIndex()):
        return len(self.profiles)

    def set_profiles(self, profiles: List[Profile]):
        self.beginResetModel()
        self.profiles = profiles
        self.endResetModel()

    def append_profile(self, profile: Profile):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.profiles.append(profile)
        self.endInsertRows()

    def remove_profile(self, profile: Profile):
        index = self.profiles.index(profile)
        self.beginRemoveRows(QModelIndex(), index, index)
        self.profiles.remove(profile)
        self.endRemoveRows()
