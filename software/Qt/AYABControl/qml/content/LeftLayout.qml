import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import QtQuick.Dialogs 1.0


Item {
    id: leftLayout
    property string propertyProjectName: "none"
    property int propertyStartNeedle: 1
    property int propertyStopNeedle: 10
    property int propertyNumberOfLines: 1
    signal sendButtonTriggered()
    signal getVersionButtonTriggered()
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    GridLayout {
        x: 10
        y: 30
        columnSpacing: 10
        rowSpacing: 10
        id: newGrid
        columns: 2
        Text {
            text: "Project Name:"
            width: 200
        }
        Text {
            text: leftLayout.propertyProjectName
            width: 200
        }
        Text {
            text: "Start Needle:"
            width: 200
        }
        Text {
            text: leftLayout.propertyStartNeedle
            width: 200
        }
        Text {
            text: "Stop Needle:"
            width: 200
        }
        Text {
            text: leftLayout.propertyStopNeedle
            width: 200
        }
        Text {
            text: "Number of Lines:"
            width: 200
        }
        Text {
            text: leftLayout.propertyNumberOfLines
            width: 200
        }
        Button {
            id: sendButton
            text: "Start"
            width: 92
            tooltip:"Start Knitting"
            onClicked: sendButtonTriggered()

        }
        Text{

        }
        Button {
            id: getVersionButton
            text: "Get Version"
            width: 92
            tooltip:"Ger AYAB Version"
            onClicked: getVersionButtonTriggered()

        }
    }
}
