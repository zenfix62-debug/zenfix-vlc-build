#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: apply_zenfix.py /path/to/vlc")

root = Path(sys.argv[1]).resolve()
repo = Path(__file__).resolve().parents[1]
qml_dir = root / "modules/gui/qt/player/qml"

for name in ("ZenfixSideMenu.qml", "ZenfixQuickControls.qml"):
    shutil.copy2(repo / "overlay" / name, qml_dir / name)


def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"patch anchor not found in {path}: {old[:100]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# Register our QML files in both supported build descriptions.
meson = root / "modules/gui/qt/meson.build"
replace_once(
    meson,
    "       'player/qml/Player.qml',\n",
    "       'player/qml/Player.qml',\n"
    "       'player/qml/ZenfixSideMenu.qml',\n"
    "       'player/qml/ZenfixQuickControls.qml',\n",
)

makefile = root / "modules/gui/qt/Makefile.am"
replace_once(
    makefile,
    "\tplayer/qml/Player.qml \\\n",
    "\tplayer/qml/Player.qml \\\n"
    "\tplayer/qml/ZenfixSideMenu.qml \\\n"
    "\tplayer/qml/ZenfixQuickControls.qml \\\n",
)

player = root / "modules/gui/qt/player/qml/Player.qml"

# Reserve real layout space for the left rail and right play queue.
replace_once(
    player,
    "        anchors {\n"
    "            left: parent.left\n"
    "            right: parent.right\n"
    "            top: (MainCtx.hasEmbededVideo && rootPlayer._controlsUnderVideo) ? topBar.bottom : parent.top\n"
    "            bottom: (MainCtx.hasEmbededVideo && rootPlayer._controlsUnderVideo) ? controlBar.top : parent.bottom\n"
    "        }\n",
    "        anchors {\n"
    "            left: parent.left\n"
    "            right: parent.right\n"
    "            top: (MainCtx.hasEmbededVideo && rootPlayer._controlsUnderVideo) ? topBar.bottom : parent.top\n"
    "            bottom: (MainCtx.hasEmbededVideo && rootPlayer._controlsUnderVideo) ? controlBar.top : parent.bottom\n"
    "            leftMargin: zenfixSideMenu.visible ? zenfixSideMenu.width + VLCStyle.margin_small : 0\n"
    "            rightMargin: playlistpopup.visible ? playlistpopup.width + VLCStyle.margin_small : 0\n"
    "        }\n",
)

# Insert the Zenfix glass side rail and the Pro Compact quick row.
replace_once(
    player,
    "    TopBar {\n        id: topBar\n",
    "    ZenfixSideMenu {\n"
    "        id: zenfixSideMenu\n"
    "        z: 7\n"
    "        visible: MainCtx.intfMainWindow.visibility !== Window.FullScreen\n"
    "        anchors {\n"
    "            top: topBar.bottom\n"
    "            left: parent.left\n"
    "            bottom: zenfixQuickControls.top\n"
    "        }\n"
    "    }\n\n"
    "    ZenfixQuickControls {\n"
    "        id: zenfixQuickControls\n"
    "        z: 7\n"
    "        visible: MainCtx.intfMainWindow.visibility !== Window.FullScreen\n"
    "        anchors {\n"
    "            left: zenfixSideMenu.right\n"
    "            right: playlistpopup.left\n"
    "            bottom: controlBar.top\n"
    "        }\n"
    "    }\n\n"
    "    TopBar {\n        id: topBar\n",
)

# Keep the native title/CSD bar but remove the old horizontal menu from it.
replace_once(
    player,
    "        showToolbar: MainCtx.hasToolbarMenu && (MainCtx.intfMainWindow.visibility !== Window.FullScreen)\n",
    "        showToolbar: false\n",
)

replace_once(
    player,
    "        textWidth: playlistVisibility.isPlaylistVisible\n"
    "                 ? rootPlayer.width - playlistpopup.width\n"
    "                 : rootPlayer.width\n",
    "        textWidth: rootPlayer.width - (playlistpopup.visible ? playlistpopup.width : 0)\n",
)

# Make the right playlist a stable docked glass panel in windowed mode.
old_playlist_anchors = """        anchors {\n            // NOTE: When the controls are pinned we display the playqueue under the topBar.\n            top: (rootPlayer._controlsUnderVideo) ? topBar.bottom\n                                                  : parent.top\n\n            right: parent.right\n            bottom: parent.bottom\n\n            bottomMargin: parent.height - rootPlayer.positionSliderY\n        }\n"""
new_playlist_anchors = """        anchors {\n            top: topBar.bottom\n            right: parent.right\n            bottom: zenfixQuickControls.top\n        }\n"""
replace_once(player, old_playlist_anchors, new_playlist_anchors)
replace_once(player, "        active: MainCtx.playqueuePanel.docked\n", "        active: true\n")

old_playlist_binding = """        //initial state value is \"\", using a binding avoid animation on startup\n        Binding on state {\n            when: playlistVisibility.started\n            value: (status === Loader.Ready && playlistVisibility.isPlaylistVisible) ? \"expanded\" : \"retracted\"\n        }\n"""
new_playlist_binding = """        Binding on state {\n            value: (MainCtx.intfMainWindow.visibility === Window.FullScreen) ? \"retracted\" : \"expanded\"\n        }\n"""
replace_once(player, old_playlist_binding, new_playlist_binding)
replace_once(player, "            useAcrylic: false\n", "            useAcrylic: true\n")
replace_once(
    player,
    "            background: Rectangle {\n                color: windowTheme.bg.primary.alpha(0.8)\n            }\n",
    "            background: Widgets.AcrylicBackground {\n"
    "                tintColor: windowTheme.bg.secondary\n"
    "                alternativeColor: windowTheme.bg.primary\n"
    "            }\n",
)

# Place VLC's real seek/play/volume/fullscreen controls inside the central column.
replace_once(
    player,
    "        anchors {\n"
    "            bottom: parent.bottom\n"
    "            left: parent.left\n"
    "            right: parent.right\n"
    "        }\n\n"
    "        hoverEnabled: true\n",
    "        anchors {\n"
    "            bottom: parent.bottom\n"
    "            left: parent.left\n"
    "            right: parent.right\n"
    "            leftMargin: zenfixSideMenu.visible ? zenfixSideMenu.width : 0\n"
    "            rightMargin: playlistpopup.visible ? playlistpopup.width : 0\n"
    "        }\n\n"
    "        hoverEnabled: true\n",
)

old_control_binding = """        //initial state value is \"\", using a binding avoid animation on startup\n        Binding on state {\n            when: playerToolbarVisibilityFSM.started\n            value: (playerToolbarVisibilityFSM.isVisible || rootPlayer._controlsUnderVideo) ? \"visible\" : \"hidden\"\n        }\n"""
new_control_binding = """        Binding on state {\n            when: playerToolbarVisibilityFSM.started\n            value: (MainCtx.intfMainWindow.visibility !== Window.FullScreen)\n                   ? \"visible\"\n                   : ((playerToolbarVisibilityFSM.isVisible || rootPlayer._controlsUnderVideo) ? \"visible\" : \"hidden\")\n        }\n"""
replace_once(player, old_control_binding, new_control_binding)

print("Zenfix UI overlay applied successfully")
