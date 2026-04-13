# app/views/cadastro_view.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                               QComboBox, QPushButton, QMessageBox)
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

class CadastroView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.setWindowTitle("Novo Cadastro")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Validador Front-end: Bloqueia números e caracteres especiais
        validador_letras = QRegularExpressionValidator(QRegularExpression(r"^[A-Za-zÀ-ÿ\s]+$"))

        self.input_nome = QLineEdit()
        self.input_nome.setValidator(validador_letras)
        
        self.input_sobrenome = QLineEdit()
        self.input_sobrenome.setValidator(validador_letras)
        
        self.combo_genero = QComboBox()
        self.combo_genero.addItems(["Masculino", "Feminino", "Outro"])
        
        self.input_data = QLineEdit(placeholderText="Ex: 15/04/1880")
        self.input_local = QLineEdit(placeholderText="Ex: Treviso")

        form.addRow("Nome:", self.input_nome)
        form.addRow("Sobrenome:", self.input_sobrenome)
        form.addRow("Gênero:", self.combo_genero)
        form.addRow("Data Nascimento:", self.input_data)
        form.addRow("Local Nascimento:", self.input_local)

        btn_salvar = QPushButton("Salvar Imigrante")
        btn_salvar.clicked.connect(self.ao_salvar)

        layout.addLayout(form)
        layout.addWidget(btn_salvar)

    def ao_salvar(self):
        # 1. Coleta os dados da tela
        nome = self.input_nome.text()
        sobrenome = self.input_sobrenome.text()
        genero = self.combo_genero.currentText()
        data = self.input_data.text()
        local = self.input_local.text()

        # 2. Verifica campos obrigatórios na UI
        if not nome or not sobrenome or not data:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos obrigatórios.")
            return

        # 3. Repassa a responsabilidade para o Controller
        try:
            self.controller.cadastrar_individuo(nome, sobrenome, genero, data, local)
            QMessageBox.information(self, "Sucesso", "Indivíduo e nascimento registrados!")
            self.limpar_campos()
        except Exception as erro:
            QMessageBox.critical(self, "Erro", str(erro))

    def limpar_campos(self):
        self.input_nome.clear()
        self.input_sobrenome.clear()
        self.input_data.clear()
        self.input_local.clear()
        self.input_nome.setFocus()