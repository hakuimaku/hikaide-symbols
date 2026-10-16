# Hikaide-Symbols

A GTK icon theme with graphite folders, folded paper files, and sculpted application icons.

![Application overview](previews/overview-apps.png)
![Folder states](previews/folder-states.png)

<details>
<summary>All icon previews</summary>

![Application icons](previews/preview-apps.png)

![Folder and places icons](previews/preview-places.png)

![File type icons](previews/preview-mimetypes.png)

![Device icons](previews/preview-devices.png)

![Status icons](previews/preview-status.png)

![Action icons](previews/preview-actions.png)

![Category icons](previews/preview-categories.png)

![Emblem icons](previews/preview-emblems.png)

</details>

## Install

Requires Python 3.9+. From the repository root:

```sh
python3 scripts/build.py
./scripts/install.sh
```

Installs to `~/.icons/Hikaide-Symbols` without root access. To update an existing installation, rebuild and run `./scripts/install.sh --replace`. Replacement resets installed artwork and accent to the build; save customizations first.

For an XDG installation, add `--xdg` to install, update, and uninstall commands.

## Setup

Select **Hikaide-Symbols** in GNOME Tweaks, Xfce Appearance, or your icon theme selector. On GNOME:

```sh
gsettings set org.gnome.desktop.interface icon-theme 'Hikaide-Symbols'
```

## Uninstall

Select another icon theme, then run:

```sh
./scripts/uninstall.sh
```

[Technical documentation](docs/README.md) · [MIT License](LICENSE)
