import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0



Item {

    id: debugLayout
    //anchors.fill: parent
    property string testName: "Hundehaufen"
    property variant testcombobox: ["Hundehaufen"]
    Rectangle {
        width: 100
        height: 62
    }
    Text {
        id: hubsi
        text: testName
    }
    ComboBox {
        id: testcombobox1
        width: 200
        model: testcombobox
    }
}


