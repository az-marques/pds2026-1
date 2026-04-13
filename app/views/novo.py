import sys
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout, 
    QLineEdit, 
    QPushButton,
    QTableWidget, 
    QTableWidgetItem, 
    QLabel, 
    QMessageBox
)

from app.db import DBManager  # Importando a lógica da Alice

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Configuração do Banco de Dados (Reutilizando o código da Alice)
        self.db = DBManager("sqlite:///database.db")

        # 2. Configurações da Janela
        self.setWindowTitle("Sistema de Genealogia - Quarta Colônia (Qt)")
        self.setMinimumSize(700, 500)

        # 3. Layout Principal
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_v = QVBoxLayout(self.widget_central)

        # 4. Formulário de Cadastro
        self.setup_formulario()

        # 5. Tabela de Indivíduos
        self.setup_tabela()

    def setup_formulario(self):
        layout_h = QHBoxLayout()
        
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")
        
        self.input_sobrenome = QLineEdit()
        self.input_sobrenome.setPlaceholderText("Sobrenome")
        
        btn_adicionar = QPushButton("Adicionar Imigrante")
        btn_adicionar.clicked.connect(self.salvar_dados) # Conexão de Sinal/Slot

        layout_h.addWidget(self.input_nome)
        layout_h.addWidget(self.input_sobrenome)
        layout_h.addWidget(btn_adicionar)
        
        self.layout_v.addLayout(layout_h)

    def setup_tabela(self):
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Sobrenome"])
        self.layout_v.addWidget(self.tabela)
        
        self.carregar_dados()

    def salvar_dados(self):
        nome = self.input_nome.text().strip()
        sobrenome = self.input_sobrenome.text().strip()

        if nome and sobrenome:
            try:
                # Chamando o método add_individuo da Alice
                self.db.add_individuo(nome, sobrenome)
                self.input_nome.clear()
                self.input_sobrenome.clear()
                self.carregar_dados()
                QMessageBox.information(self, "Sucesso", "Cadastrado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")
        else:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")

    def carregar_dados(self):
        # Usando o get_individuos da Alice
        pessoas = self.db.get_individuos()
        self.tabela.setRowCount(0)
        
        for p in pessoas:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            self.tabela.setItem(row, 0, QTableWidgetItem(str(p.id)))
            self.tabela.setItem(row, 1, QTableWidgetItem(p.nome))
            self.tabela.setItem(row, 2, QTableWidgetItem(p.sobrenome))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JanelaPrincipal()
    window.show()
    sys.exit(app.exec())