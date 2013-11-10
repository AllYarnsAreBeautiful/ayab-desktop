import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0



Item {

    id: leftLayout
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    property string testName: "Hundehaufen"

    Text {
        id: hubsi
        text: testName
    }
}
