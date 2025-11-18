<!--
SPDX-FileCopyrightText: 2024 Ondsel <development@ondsel.com>

SPDX-License-Identifier: LGPL-2.0-or-later
-->

# Ondsel Lens Addon

This FreeCAD addon provides a convenient way to manage designs in [Ondsel Lens
server](https://github.com/FreeCAD/Ondsel-Server) instances.  An Ondsel Lens
server is a server that can be hosted by yourself to manage and share FreeCAD
files.

## Installation

The Ondsel Lens addon is available through the FreeCAD Addon Manager.

Open the Addon manager. Find in the list 'Ondsel-Lens' and install it.  The
installation will require restarting FreeCAD.  You should then see the Ondsel
Addon in its own tab besides Start.  You can type Ctrl-L to show it.

### Dependencies

The addon requires a couple of additional Python dependencies that should be
installed automatically by the FreeCAD addon manager.

If you have a problem with dependencies you can install them manually by: Open
the Python console in FreeCAD and enter the following code

```
import addonmanager_dependency_installer
depsInstaller = addonmanager_dependency_installer.DependencyInstaller([],['pyjwt','requests','tzlocal'],[])
depsInstaller._install_python_packages()
```

Note: ```pip install jwt``` installs the wrong library. You need ```pip install pyjwt```.

## First Use

### Overview

The addon introduces the notion of *workspaces*. Workspaces are collections of
files that constitute a project and are hosted on the Ondsel Lens server.  To
start working and collaborating on FreeCAD designs, you must create an account
on an Ondsel Lens server.

### Creating an account

Visit an Ondsel Lens server in a web browser and sign up.  There are four
pieces of information to remember:
- the URL of the Lens server, for example `http://localhost:3000`,
- the URL of the Lens API, for example `http://localhost:3030`,
- the email address with which you signed up, and
- the password.

### Create a profile

Once an account is created, you can open the Ondsel Lens Addon by switching to
the tab "Ondsel Lens" or press Ctrl-L in FreeCAD.  In the top left, click on
the main button that says "(no profile selected)" and choose "Manage profiles".
There you can create a profile with a name that is meaningful to you and
consists of alphanumeric characters, dashes, or underscores, for example
"localhost".  If the suggested values for the Ondsel Lens and Ondsel API url
are correct, you can skip these values.  Finally, add your email address, and
press OK.  You can then close the "Manage Profiles" dialog.

### Log in

Now that you have created a profile, you can choose this profile by clicking
the main button in the top left and choosing Profile and then the profile that
you've just created.  This changes the button color from grey to yellow which
means that you are in the logged out state.

In the main button, you can now choose "Log in" that shows a dialog where you
can enter the password for the Ondsel Lens server.  Filling in the password and
pressing OK should log you in to the server and the color of the button should
change from yellow to orange, which means that you are logged in.

You can now access your workspace "Default (Personal)" and from here you can
save files and access them from another location.  In addition, you can browse
examples curated for this server (the Ondsel Start tab), browse your bookmarks,
search for models, or view the most recent models that are shared on Lens.

![image](https://github.com/user-attachments/assets/d59fb797-bdc8-44a7-b84c-dcec3a2e30a4)

### Workspaces

In tab "Workspaces" you should see a list of workspaces available to you.  A
workspace maps to a folder on your hard drive and contains files and folders.
Files can be in five different states:

- "Untracked": Ondsel Lens does not track this file
- "Not downloaded": The file is only available on Lens
- "Synced": the local version is in sync with the Ondsel Lens version
- "Local copy newer": The local version is newer than the server one
- "Lens copy newer": The server version is newer than the local one

By means of download and upload actions, files can be synchronized with the
Lens service and Lens maintains different versions for files.  One version of
each file is marked as the active version which typically is the last
version of a file.  Uploading a new version makes that version the active one.

The addon shows additional details for FreeCAD files.  It shows a thumbnail
of the file, the version information and share links of the file.

### Sharing Links

A file that is hosted on the Ondsel Lens server can be shared and viewed
through the website. Sharing links can also be fine-tuned to permit the
recipient certain privileges including download formats.

### Offline workflow

The addon also allows for an offline workflow.  If a user is logged out, it is
still possible to work on the files of workspaces that are currently on disk.
As soon as a user logs into Lens, the user has the ability to upload the new
versions to Lens.

## History

The [Ondsel Lens server](https://github.com/FreeCAD/Ondsel-Server) is the
server software for the cloud service `lens.ondsel.com` from company
[Ondsel](https://web.archive.org/web/20250929053407/https://ondsel.com/) that
was run by [Brad Collette (sliptonic)](https://www.linkedin.com/in/sliptonic).
This addon was shipped with Ondsel's flavor of FreeCAD called Ondsel ES and
aimed to integrate Ondsel ES and the Lens platform.  The addon was also
available in FreeCAD's Addon Manager.

Unfortunately, Ondsel had to [shut
down](https://web.archive.org/web/20250929053313/https://ondsel.com/blog/goodbye/)
but since then the server software has become open source under the AGPL
license.  The addon had always been open source.  Both software packages and
its documentation are now incorporated into the [FreeCAD GitHub
organization](https://github.com/FreeCAD).

Development of the server is now continuing under the [Ondsel Onward
Fund](https://blog.freecad.org/2025/02/14/the-ondsel-onwards-fund/) and
development of this addon as part of the [NLnet](https://nlnet.nl/) grant
[Lens/FreeCAD integration](https://nlnet.nl/project/Lens-FreeCAD-integration/).

![Logo Lens/FreeCAD Integration](https://nlnet.nl/project/Lens-FreeCAD-integration/freecad.hex.svg)

## License

This repository is REUSE compliant.

## Contact

If you're interested in using or developing the addon, feel free to create or
view issues in the [issue
tracker](https://github.com/FreeCAD/Ondsel-Lens-Addon/issues).  The best place
to talk with us about bugs and features is on our [Discord
Channel](https://discord.com/channels/870877411049357352/1313153066266267688).
