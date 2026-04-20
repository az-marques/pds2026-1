# app/views/cadastro_view.py
from PySide6.QtCore import QRegularExpression, QDate
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QLabel,
    QFormLayout, 
    QLineEdit, 
    QComboBox,
    QCheckBox,
    QPushButton, 
    QMessageBox
)

from app.models.enums import GenderEnum

class CadastroIndiVw(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller=controller
        
        self.setWindowTitle("Dados cadastrais do indivíduo")
        self.setMinimumSize(700, 500)
        
        self.form_setup()
        
    def form_setup(self):
        layoutv=QVBoxLayout(self)
        form=QFormLayout()
        # self.txt=QLabel("Digite os dados de cadastro do individuo")
        # Validador Front-end: Bloqueia números e caracteres especiais
        validador_letras = QRegularExpressionValidator(QRegularExpression(r"^[A-Za-zÀ-ÿ\s]+$"))
        
        self.input_fname=QLineEdit()
        self.input_fname.setPlaceholderText("Digite seu primeiro nome")
        self.input_fname.setValidator(validador_letras)
        
        self.input_lname=QLineEdit()
        self.input_lname.setPlaceholderText("Digite seu sobrenome")
        self.input_lname.setValidator(validador_letras)
        
        # form.addRow("Nome*:", self.input_fname)
        # form.addRow("Sobrenome*:", self.input_lname)
        
        # para genero=combobox + Enum
        self.combo_box_genero=QComboBox()
        for genero in GenderEnum:
            # add item (txt visivel, objeto pyhton)
            self.combo_box_genero.addItem(genero.value, genero)
            
        self.chk_vivo=QCheckBox("A pessoa está viva")
        self.chk_vivo.setChecked(True)
        
        form.addRow("Nome*:", self.input_fname)
        form.addRow("Sobrenome*:", self.input_lname)
        form.addRow("Gênero:", self.combo_box_genero)
        form.addRow("", self.chk_vivo)
        
        save_btn=QPushButton("Adicionar pessoa")
        save_btn.clicked.connect(self.salvar_dados)
        
        layoutv.addLayout(form)
        layoutv.addWidget(save_btn)
    
    def salvar_dados(self):
        # coleta os dados do form da tela
        # envia para o Controller em formato de dicionario
        
        # Pega o objeto GeneroEnum "invisível" anexado à seleção atual
        gen_select = self.combo_box_genero.currentData()
        
        dados = {
            "nome": self.input_fname.text(),
            "sobrenome": self.input_lname.text(),
            "genero": gen_select,
            "vivo": self.chk_vivo.isChecked()   
        }
        
        if not dados["nome"] or not dados["sobrenome"] or not dados:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos obrigatorios marcados com *")
            return
        
        # if not dados["nome"] or not dados["sobrenome"] or not dados:
        #     QMessageBox.warning(self, "Aviso", "Preencha todos os campos obrigatórios, marcados com (*)")
        #     retur
        try:
        # Passamos o dicionário para o Controller
            self.controller.cria_individuo(dados)
            QMessageBox.information(self, "Sucesso", "Cadastrado com sucesso!")
        except ValueError as err_validacao:
        # O Pydantic barrou a entrada (ex: números no nome)
            QMessageBox.warning(self, "Dados Inválidos", str(err_validacao))
        except Exception as err_geral:
        # O banco de dados falhou
            QMessageBox.critical(self, "Erro", str(err_geral))
    
    def limpar_campos(self):
        self.input_fname.clear()
        self.input_lname.clear()
        
            
            

# # Trecho dentro de app/views/cadastro_view.py, no método ao_salvar:

# def ao_salvar(self):
#     # Preparamos um dicionário simples com os dados da tela
#     dados = {
#         "nome": self.input_nome.text(),
#         "sobrenome": self.input_sobrenome.text(),
#         "genero": self.combo_genero.currentText()[0], # Pega apenas a 1ª letra (M, F, O)
#         "data_nasc": self.input_data.text(),
#         "local_nasc": self.input_local.text()
#     }


        



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = JanelaPrincipal()
#     window.show()
#     sys.exit(app.exec())
        
        
        
        
        
        

        
        
        # self.input_fname.setPlaceholderText("Digite seu primeiro nome")
        
        
        
        
        



#class C



# from db import DBManager  # Importa a lógica da Alice

# Instancia o gerenciador apontando para um arquivo local
# database = DBManager("sqlite:///database.db")