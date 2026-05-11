import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QFormLayout, QLineEdit, QComboBox, 
                               QPushButton, QGroupBox, QMessageBox)
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

class JanelaCadastro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Genealogia - Cadastro")
        self.setMinimumWidth(500)

        # Configuração do Widget Central e Layout Principal
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QVBoxLayout(self.widget_central)

        # Expressão Regular para nomes: apenas letras, acentos e espaços
        # O Qt utiliza QRegularExpression para isso
        self.regex_nomes = QRegularExpression(r"^[A-Za-zÀ-ÿ\s]+$")
        self.validador_nomes = QRegularExpressionValidator(self.regex_nomes)

        self.construir_dados_pessoais()
        self.construir_evento_nascimento()
        self.construir_eventos_opcionais()
        self.construir_botoes()

    def construir_dados_pessoais(self):
        grupo = QGroupBox("Dados Pessoais (Obrigatório)")
        layout = QFormLayout()

        self.input_nome = QLineEdit()
        self.input_nome.setValidator(self.validador_nomes) # Aplica a validação na UI
        self.input_nome.setPlaceholderText("Apenas letras")

        self.input_sobrenome = QLineEdit()
        self.input_sobrenome.setValidator(self.validador_nomes) # Aplica a validação na UI

        self.combo_genero = QComboBox()
        self.combo_genero.addItems(["Selecione...", "Masculino", "Feminino", "Outro"])

        layout.addRow("Nome:", self.input_nome)
        layout.addRow("Sobrenome:", self.input_sobrenome)
        layout.addRow("Género:", self.combo_genero)

        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def construir_evento_nascimento(self):
        grupo = QGroupBox("Nascimento (Obrigatório)")
        layout = QFormLayout()

        self.input_data_nasc = QLineEdit()
        self.input_data_nasc.setPlaceholderText("Ex: 15/04/1880 ou Circa 1880")
        
        self.input_local_nasc = QLineEdit()
        self.input_local_nasc.setPlaceholderText("Ex: Treviso, Itália")

        layout.addRow("Data:", self.input_data_nasc)
        layout.addRow("Local:", self.input_local_nasc)

        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def construir_eventos_opcionais(self):
        grupo = QGroupBox("Eventos Opcionais (Batismo e Falecimento)")
        layout = QFormLayout()

        self.input_data_batismo = QLineEdit()
        self.input_local_batismo = QLineEdit()
        
        self.input_data_obito = QLineEdit()
        self.input_local_obito = QLineEdit()

        layout.addRow("Data de Batismo:", self.input_data_batismo)
        layout.addRow("Local de Batismo:", self.input_local_batismo)
        layout.addRow("Data de Falecimento:", self.input_data_obito)
        layout.addRow("Local de Falecimento:", self.input_local_obito)

        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def construir_botoes(self):
        layout = QHBoxLayout()
        
        btn_limpar = QPushButton("Limpar")
        btn_limpar.clicked.connect(self.limpar_formulario)
        
        btn_salvar = QPushButton("Salvar Imigrante")
        btn_salvar.setDefault(True) # Destaca o botão principal
        btn_salvar.clicked.connect(self.salvar_dados)

        layout.addWidget(btn_limpar)
        layout.addWidget(btn_salvar)
        self.layout_principal.addLayout(layout)

    def limpar_formulario(self):
        for input_field in self.findChildren(QLineEdit):
            input_field.clear()
        self.combo_genero.setCurrentIndex(0)

    def salvar_dados(self):
        """
        Função chamada quando o botão Salvar é clicado.
        Aqui fazemos a validação final antes de enviar para o DBManager.
        """
        nome = self.input_nome.text().strip()
        sobrenome = self.input_sobrenome.text().strip()
        genero = self.combo_genero.currentText()
        data_nasc = self.input_data_nasc.text().strip()
        local_nasc = self.input_local_nasc.text().strip()

        # Validação de campos obrigatórios
        if not nome or not sobrenome:
            QMessageBox.warning(self, "Aviso", "Nome e Sobrenome são obrigatórios!")
            self.input_nome.setFocus()
            return

        if genero == "Selecione...":
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um género.")
            return

        if not data_nasc or not local_nasc:
            QMessageBox.warning(self, "Aviso", "Os dados de nascimento são obrigatórios!")
            self.input_data_nasc.setFocus()
            return

        # Montagem do dicionário de dados (simulando o envio para o banco)
        dados = {
            "nome": nome,
            "sobrenome": sobrenome,
            "genero": genero,
            "nascimento": {"data": data_nasc, "local": local_nasc},
            "batismo": {"data": self.input_data_batismo.text(), "local": self.input_local_batismo.text()},
            "obito": {"data": self.input_data_obito.text(), "local": self.input_local_obito.text()}
        }

        # Aqui você chamaria o db.py da Alice, por exemplo:
        # self.db.add_individuo(nome, sobrenome)
        # E depois precisaria de métodos para adicionar os eventos no banco.

        QMessageBox.information(self, "Sucesso", f"Dados de {nome} {sobrenome} prontos para gravação na base de dados!")
        self.limpar_formulario()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaCadastro()
    janela.show()
    sys.exit(app.exec())