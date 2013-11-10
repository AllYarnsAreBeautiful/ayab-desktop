import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0



Item {

    id: designLayout
    property int startNeedle: 0
    property int stopNeedle: 10
    property int lines: 1
    Grid {

        x: 10; y: 10
        rows: designLayout.lines; columns: designLayout.stopNeedle-designLayout.startNeedle+1; spacing: 1
        Repeater {
            id: rectangleRepeater
            model: (designLayout.stopNeedle-designLayout.startNeedle+1)*lines
            Rectangle {
                id: pixel
                width: 4
                height: 4
                color: "lightgreen"
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    onClicked: {
                        parent.color = "black"
                    }
                }
            }
        }
    }
}
