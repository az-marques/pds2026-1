import QtQuick
import QtQuick.Controls

ApplicationWindow{
    visible: true
    width: 800
    height: 600
    title: "Sistema"

    StackView{
        id: stack
        anchors.fill: parent
        initialItem: HomePage {}
    }

}