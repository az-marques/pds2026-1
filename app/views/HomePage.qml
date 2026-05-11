import QtQuick
import QtQuick.Controls

Page{
    title: "inicio"

    Column{
        anchors.centerIn: parent
        spacing: 20

        Label{
            text: "sistrema genealog"
            font.pixelSize: 24
        }

        Button{
            text: "cadastrar pessoa"
            onClicked{
                stack: push("CadastroPesForm.qml")
            }

        }
    }
}