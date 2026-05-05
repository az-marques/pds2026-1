import QtQuick
import QtQuick.Controls

Page {
    title: "Cadastro de Pessoa"

    Column {
        anchors.centerIn: parent
        spacing: 10
        width: 300

        TextField {
            id: firstName
            placeholderText: "Nome"
        }

        TextField {
            id: surname
            placeholderText: "Sobrenome"
        }

        ComboBox {
            id: gender
            model: ["male", "female", "other", "unknown"]
        }

        Button {
            text: "Salvar"

            onClicked: {
                if (firstName.text === "" || surname.text === "") {
                    console.log("Preencha todos os campos")
                    return
                }

                console.log("Dados enviados:")
                console.log(firstName.text, surname.text, gender.currentText)

                stack.pop()
            }
        }

        Button {
            text: "Voltar"
            onClicked: stack.pop()
        }
    }
}