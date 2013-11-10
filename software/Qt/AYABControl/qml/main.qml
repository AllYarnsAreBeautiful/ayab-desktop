import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import QtQuick.Dialogs 1.0
import "content"
ApplicationWindow {
    id: idAYABControl
    title: "AYABControl 0.1"
    width: 1024//mainLayout.implicitWidth + 2 * mainLayout.columnSpacing
    height: 768//mainLayout.implicitHeight + 2 * mainLayout.rowSpacing
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * mainLayout.columnSpacing
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * mainLayout.rowSpacing + menuHeight
    visibility: "AutomaticVisibility"

    readonly property int menuHeight: idAYABControl.height - mainLayout.height - 2 * mainLayout.rowSpacing

    property alias settingsSerialPortComboboxText: serialPortCombobox.currentText
    property variant serialPortComboboxModel: ["no Serial Ports"]

    property int designerNumberOfLines: 1
    property int designerStartNeedle: 1
    property int designerStopNeedle: 100

    property alias newStartNeedle: startNeedleSpinBox.value
    property alias newStopNeedle: stopNeedleSpinBox.value
    property alias newNumberOfLines: numberOfLinesSpinbox.value

    signal cutTriggered()
    signal copyTriggered()
    signal pasteTriggered()

    signal aboutTriggered()

    signal newTriggered()
    signal newOKTriggered()
    signal settingsTriggered()
    signal settingsOKTriggered()
    // actions ///////////////////////////////////////////////////////////////

    Action {
        id: newAction
        text: "&New"
        shortcut: "Ctrl+N"
        onTriggered: idAYABControl.newTriggered()
    }

    Action {
        id: settingsAction
        text: "&Settings"
        onTriggered: idAYABControl.settingsTriggered()
    }


    Action {
        id: quitAction
        text: "&Quit"
        shortcut: "Ctrl+Q"
        iconSource: "exit.png"
        iconName: "application-exit"
        onTriggered: Qt.quit()
    }

    Action {
        id: cutAction
        text: "Cu&t"
        shortcut: "Ctrl+X"
        iconSource: "edit-cut.png"
        iconName: "edit-cut"
        onTriggered: idAYABControl.cutTriggered()
    }

    Action {
        id: copyAction
        text: "&Copy"
        shortcut: "Ctrl+C"
        iconSource: "edit-copy.png"
        iconName: "edit-copy"
        onTriggered: idAYABControl.copyTriggered()
    }

    Action {
        id: pasteAction
        text: "&Paste"
        shortcut: "Ctrl+V"
        iconSource: "edit-paste.png"
        iconName: "edit-paste"
        onTriggered: idAYABControl.pasteTriggered()
    }

    Action {
        id: aboutAction
        text: "&About AYABControl..."
        iconSource: "accessories-calculator.png"
        iconName: "accessories-calculator"
        onTriggered: idAYABControl.aboutTriggered()
    }

    // main menu /////////////////////////////////////////////////////////////

    menuBar: MenuBar {
        id: mainMenu
        Menu {
            title: "&File"
            MenuItem { action: newAction }
            MenuItem { action: quitAction }
        }
        Menu {
            title: "&Edit"
            MenuItem { action: settingsAction }
            MenuItem { action: cutAction }
            MenuItem { action: copyAction }
            MenuItem { action: pasteAction }
        }
        Menu {
            title: "&Help"
            MenuItem { action: aboutAction }
        }
    }

    // main layout ///////////////////////////////////////////////////////////


    GridLayout {
        id: mainLayout
        anchors.fill: parent
        columns: 2
        LeftLayout{
            id: leftLayoutID
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            width: 200
        }

        TabView {
            id:rightLayout
            //width: 640
            //height: 480
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.left: leftLayoutID.right
            anchors.margins: Qt.platform.os === "osx" ? 12 : 2


            Tab {
                id: debugTab
                title: "Debug"
                DebugTab {
                    id: debugLayoutID
                }
            }
            Tab {
                id: designerTab
                title: "Designer"
                DesignerTab {
                    id: designerLayoutID
                    lines: idAYABControl.designerNumberOfLines
                    startNeedle: idAYABControl.designerStartNeedle
                    stopNeedle: idAYABControl.designerStopNeedle
                }
            }
        }

    }

    // functions /////////////////////////////////////////////////////////////

    function showAboutDialog() {
        aboutBox.show()
    }

    function showSettingsDialog() {
        settingsBox.show()
    }

    function settingsDialogOKClicked() {
        idAYABControl.settingsOKTriggered()
        settingsBox.close()
    }

    function showNewDialog() {
        newBox.show()
    }

    function newDialogOKClicked() {
        idAYABControl.newOKTriggered()
        newBox.close()
    }
    // dialogs ///////////////////////////////////////////////////////////////

    ApplicationWindow {
        id: aboutBox

        maximumWidth: 280
        maximumHeight: 120
        minimumWidth: maximumWidth
        minimumHeight: maximumHeight
        width: maximumWidth
        height: maximumHeight

        title: "About AYABControl"
        flags: Qt.Dialog | Qt.WindowCloseButtonHint
        modality: Qt.WindowModal
        visible: false

        ColumnLayout {
            id: dialogLayout
            anchors.fill: parent
            anchors.margins: spacing

            RowLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignCenter

                Label {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    anchors.centerIn: parent
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.WordWrap

                    text: "<b>AYABControl</b>" +
                          "<p>This is AYABControl Application</p>"
                }
            }

            Button {
                text: "Ok"
                isDefault: true
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                onClicked: aboutBox.close()
            }
            Keys.onReturnPressed: aboutBox.close()
            focus: true
        }
    }

    ApplicationWindow {
        id: settingsBox

        maximumWidth: 280
        maximumHeight: 120
        minimumWidth: maximumWidth
        minimumHeight: maximumHeight
        width: maximumWidth
        height: maximumHeight

        title: "AYABControl Settings"
        flags: Qt.Dialog | Qt.WindowCloseButtonHint
        modality: Qt.WindowModal
        visible: false

        ColumnLayout {
            id: settingsLayout
            anchors.fill: parent
            anchors.margins: spacing

            GridLayout {
                id: grid
                columns: 2
                Text { text: "Serial Port:" }
                ComboBox {
                    id: serialPortCombobox
                    width: 200
                    model: serialPortComboboxModel
                }


            }

            Button {
                text: "Ok"
                isDefault: true
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                onClicked: idAYABControl.settingsDialogOKClicked()
            }
            Keys.onReturnPressed: idAYABControl.settingsDialogOKClicked()
            focus: true
        }
    }



    ApplicationWindow {
        id: newBox

        maximumWidth: 280
        maximumHeight: 200
        minimumWidth: maximumWidth
        minimumHeight: maximumHeight
        width: maximumWidth
        height: maximumHeight

        title: "New Knitting"
        flags: Qt.Dialog | Qt.WindowCloseButtonHint
        modality: Qt.WindowModal
        visible: false

        ColumnLayout {
            id: newLayout
            anchors.fill: parent
            anchors.margins: spacing

            GridLayout {
                id: newGrid
                columns: 2
                Text {
                    text: "Name:"
                    width: 200
                }
                TextField {
                    id: projectNameTextField
                    width: 200
                }
                Text {
                    text: "Start Needle:"
                    width: 200

                }
                SpinBox {
                    id: startNeedleSpinBox
                    maximumValue : 199
                    minimumValue : 1
                }
                Text {
                    text: "Stop Needle:"
                    width: 200
                }
                SpinBox {
                    id: stopNeedleSpinBox
                    maximumValue : 200
                    minimumValue : 2
                }
                Text {
                    text: "Number of Lines"
                    width: 200
                }
                SpinBox {
                    id: numberOfLinesSpinbox

                    maximumValue : 255
                    minimumValue : 1
                }


            }

            Button {
                text: "Ok"
                isDefault: true
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                onClicked: idAYABControl.newDialogOKClicked()
            }
            Keys.onReturnPressed: idAYABControl.settingsDialogOKClicked()
            focus: true
        }
    }
}
