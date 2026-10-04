/*****************************************************************************
 * ZenfixSideMenu.qml
 * Native QML menu rail for Zenfix VLC.
 *****************************************************************************/
import QtQuick
import QtQuick.Controls
import QtQuick.Templates as T

import VLC.MainInterface
import VLC.Style
import VLC.Widgets as Widgets
import VLC.Menus

FocusScope {
    id: root

    implicitWidth: VLCStyle.dp(176, VLCStyle.scale)

    readonly property var menuIds: [
        QmlMenuBar.MEDIA,
        QmlMenuBar.PLAYBACK,
        QmlMenuBar.AUDIO,
        QmlMenuBar.VIDEO,
        QmlMenuBar.SUBTITLE,
        QmlMenuBar.TOOL,
        QmlMenuBar.VIEW,
        QmlMenuBar.HELP
    ]

    readonly property var menuIcons: [
        VLCIcons.dropzone,
        VLCIcons.play_filled,
        VLCIcons.volume_high,
        VLCIcons.topbar_video,
        VLCIcons.audiosub,
        VLCIcons.effect_filter,
        VLCIcons.grid,
        VLCIcons.info
    ]

    property int openedIndex: -1

    ColorContext {
        id: theme
        colorSet: ColorContext.Window
    }

    Widgets.AcrylicBackground {
        anchors.fill: parent
        tintColor: theme.bg.secondary
        alternativeColor: theme.bg.primary
    }

    QmlMenuBar {
        id: nativeMenu
        ctx: MainCtx
        menubar: menuColumn
        onMenuClosed: root.openedIndex = -1
    }

    Column {
        id: menuColumn
        anchors.fill: parent
        anchors.topMargin: VLCStyle.margin_small
        spacing: VLCStyle.margin_xxxsmall

        Repeater {
            model: root.menuIds.length

            T.MenuItem {
                id: menuButton
                required property int index

                width: menuColumn.width
                height: VLCStyle.dp(50, VLCStyle.scale)
                leftPadding: VLCStyle.margin_normal
                rightPadding: VLCStyle.margin_small
                hoverEnabled: true

                text: nativeMenu.menuEntryTitle(root.menuIds[index]).replace("&", "")
                font.pixelSize: VLCStyle.fontSize_normal

                contentItem: Row {
                    spacing: VLCStyle.margin_small

                    Widgets.IconLabel {
                        anchors.verticalCenter: parent.verticalCenter
                        width: VLCStyle.icon_normal
                        text: root.menuIcons[index]
                        color: menuButton.hovered || root.openedIndex === index
                               ? theme.accent
                               : theme.fg.primary
                    }

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: menuButton.text
                        color: theme.fg.primary
                        font: menuButton.font
                        elide: Text.ElideRight
                    }
                }

                background: Rectangle {
                    radius: VLCStyle.dp(8, VLCStyle.scale)
                    color: menuButton.hovered || root.openedIndex === index
                           ? Qt.rgba(1.0, 0.37, 0.02, 0.16)
                           : "transparent"
                    border.width: root.openedIndex === index ? 1 : 0
                    border.color: theme.accent
                }

                onClicked: {
                    root.openedIndex = index
                    nativeMenu.popupMenuEntry(menuButton, root.menuIds[index])
                }
            }
        }
    }
}
