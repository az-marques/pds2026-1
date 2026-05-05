import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    title: "Hello World"
    visible: true
    width: 500
    height: 500
    font.pixelSize: 24
    
    // "CSS" aplicado diretamente na janela (Cor de fundo)
    color: "#f4f4f9"

    Text {
        text: "Hello World, QtQuick"

    }

    Button {
        text: "ClickMe"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }
}