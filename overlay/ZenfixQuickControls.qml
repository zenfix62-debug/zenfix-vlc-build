/*****************************************************************************
 * ZenfixQuickControls.qml
 * Pro Compact quick access row.
 *****************************************************************************/
import QtQuick
import QtQuick.Controls
import QtQuick.Templates as T
import QtQuick.Layouts

import VLC.MainInterface
import VLC.Style
import VLC.Widgets as Widgets
import VLC.Menus
import VLC.Player

FocusScope {
    id: root

    implicitHeight: VLCStyle.dp(66, VLCStyle.scale)

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
        menubar: quickRow
    }

    RowLayout {
        id: quickRow
        anchors.fill: parent
        anchors.margins: VLCStyle.margin_small
        spacing: VLCStyle.margin_small

        ZenfixQuickButton {
            Layout.fillWidth: true
            iconText: VLCIcons.volume_high
            labelText: qsTr("Audio Track")
            valueText: qsTr("Select")
            onClicked: nativeMenu.popupMenuEntry(this, QmlMenuBar.AUDIO)
        }

        ZenfixQuickButton {
            Layout.fillWidth: true
            iconText: VLCIcons.audiosub
            labelText: qsTr("Subtitles")
            valueText: qsTr("Select")
            onClicked: nativeMenu.popupMenuEntry(this, QmlMenuBar.SUBTITLE)
        }

        ZenfixQuickButton {
            Layout.fillWidth: true
            iconText: VLCIcons.faster
            labelText: qsTr("Playback Speed")
            valueText: qsTr("%1x").arg(+Player.rate.toFixed(2))
            onClicked: nativeMenu.popupMenuEntry(this, QmlMenuBar.PLAYBACK)
        }

        ZenfixQuickButton {
            Layout.fillWidth: true
            iconText: VLCIcons.list
            labelText: qsTr("Chapters")
            valueText: qsTr("Playback menu")
            onClicked: nativeMenu.popupMenuEntry(this, QmlMenuBar.PLAYBACK)
        }
    }

    component ZenfixQuickButton: T.Button {
        id: button

        property string iconText
        property string labelText
        property string valueText

        implicitHeight: VLCStyle.dp(46, VLCStyle.scale)
        hoverEnabled: true
        leftPadding: VLCStyle.margin_small
        rightPadding: VLCStyle.margin_small

        contentItem: Row {
            spacing: VLCStyle.margin_small

            Widgets.IconLabel {
                anchors.verticalCenter: parent.verticalCenter
                text: button.iconText
                color: button.hovered ? theme.accent : theme.fg.primary
            }

            Column {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 1

                Text {
                    text: button.labelText
                    color: theme.fg.primary
                    font.pixelSize: VLCStyle.fontSize_small
                    font.weight: Font.DemiBold
                    elide: Text.ElideRight
                }

                Text {
                    text: button.valueText
                    color: theme.fg.secondary
                    font.pixelSize: VLCStyle.fontSize_xsmall
                    elide: Text.ElideRight
                }
            }
        }

        background: Rectangle {
            radius: VLCStyle.dp(8, VLCStyle.scale)
            color: button.hovered ? Qt.rgba(1.0, 0.37, 0.02, 0.13)
                                  : Qt.rgba(1.0, 1.0, 1.0, 0.035)
            border.width: 1
            border.color: button.hovered ? theme.accent : Qt.rgba(1.0, 1.0, 1.0, 0.09)
        }
    }
}
