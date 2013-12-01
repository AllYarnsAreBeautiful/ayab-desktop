import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import QtQuick.Dialogs 1.0



Item {

    id: designLayout
    property int startNeedle: 0
    property int stopNeedle: 10
    property int lines: 1
    property int needleToSet: 0
    property int lineToSet: 0
    property bool valueToSet: false
    signal signalSetPixel()
    Grid {
        id: pixelGrid
        x: 10; y: 10
        rows: designLayout.lines; columns: designLayout.stopNeedle-designLayout.startNeedle+1; spacing: 1
        Repeater {
            id: rectangleRepeater
            model: ((designLayout.stopNeedle-designLayout.startNeedle)+1)*lines
            Rectangle {
                property bool set: false
                id: pixel
                width: 4
                height: 4
                color: "lightgreen"
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    onClicked: {
                        if(parent.set === false)
                        {
                            parent.color = "black"
                            parent.set = true
                        }
                        else
                        {
                            parent.color = "lightgreen"
                            parent.set = false
                        }
                        needleToSet = index % ((designLayout.stopNeedle-designLayout.startNeedle)+1) + startNeedle - 1
                        lineToSet = Math.floor(index / ((designLayout.stopNeedle-designLayout.startNeedle)+1))
                        valueToSet = pixel.set
                        signalSetPixel()

                    }
                }
            }
        }
    }
}
