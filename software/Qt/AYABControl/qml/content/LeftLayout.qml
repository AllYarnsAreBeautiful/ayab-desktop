import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import QtQuick.Dialogs 1.0
Item {
    property string propertyProjectName: "none"
    property int propertyStartNeedle: 1
    property int propertyStopNeedle: 10
    property int propertyNumberOfLines: 1
    id: leftLayout
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    GridLayout {
        y: 50
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
    }
}
