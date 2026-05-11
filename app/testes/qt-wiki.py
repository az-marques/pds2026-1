# QT vem de um framework de mesmo nome do C++

# PyQT = pertence a uma empresa q cobra licenca de uso comercial

# PySide = fork do QT; pertence a outra empresa; totalmente livre
# Acesse a documentacao por QT(Cute) for Python https://doc.qt.io/qtforpython-6/

# instalamos com 'pip install pyside6'
# teste as versoes com:
# import PySide6.QtCore
# print(PySide6.__version__)
# print(PySide6.QtCore.__version__)

# Core = nao eh interface grafica de usuario (GUI)
#from PySide6 import QtCore
from PySide6.QtCore import QObject, Signal, Slot

# GUI = elementos que podem ou nao ser de GUI
from PySide6 import QtGui

# Widget = qualquer elemento de GUI, tal como botao, rotulo, imagem ou aquelas coisa de preencher
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout
)
import sys

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.win_title="Genealogia Italiana"
        self.setWindowTitle(self.win_title)
        
        # instanciamos um objeto chamado texto da classe chamada QLabel
        self.texto=QLabel("Digite seu nome: ")
        self.entrada=QLineEdit()
        
        self.result=QLabel("")
    
        self.btn=QPushButton("Clique aqui!")
        
        self.layout=QVBoxLayout(self)
        # layout vertical
        self.layout.addWidget(self.texto)
        self.layout.addWidget(self.entrada)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.result)
        
        # evento (funcao) que manipula botao
        self.btn.clicked.connect(self.fn_saudacao)  
        
    @Slot()
    def fn_saudacao(self):
        nome=self.entrada.text()
        if nome:
            self.result.setText(f"Olá, {nome}!")
        else:
            self.result.setText("Hello World!")
        
if __name__== '__main__':
    app=QApplication([])
    px=500
    py=180

    janela=JanelaPrincipal()
    # janela.setWindowTitle("Genealogia Italiana")
    # dimensoes do widget em pixels    
    janela.resize(px, py)
    # para mostrar nosso widget de texto chamamos o seu método show()
    janela.show()
    # entra no loop de eventos ate que a aplicacao seja encerrada
    app.exec() 




        # layout horizontal
        # self.hbox=QHBoxLayout(self)
        # self.hbox.addWidget(self.texto)
        # self.hbox.addWidget(self.entrada)
        
        # self.layout=QVBoxLayout(self)
        # self.layout.addWidget(self.texto)
        # self.layout.addWidget(self.btn) 
        

        # layout vertical
        # self.vbox=QVBoxLayout(self)
        # self.vbox.addLayout(self.hbox)
        # self.vbox.addWidget(self.btn)
        # self.vbox.addWidget(self.result)