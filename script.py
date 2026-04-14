# main.py
import sys
from PySide6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from app.db import Base
from app.models.tabelas import Base
from app.models.tabelas import Individuo

from app.views.cadastro_indi_vw import CadastroIndiVw
from app.controllers.individuo_controller import IndividuoController


def main():
    # 1. Configuração do Banco de Dados (PostgreSQL mapeado no .env)
    # Por enquanto usando SQLite para exemplificar o teste local
    engine = create_engine("sqlite:///banco_testes.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    # 2. Inicializa o Controller passando o acesso ao banco
    controller=IndividuoController(Session)
    # controller = IndividuoController(Session)
    # 3. Inicializa a Interface Gráfica passando o Controller
    app = QApplication(sys.argv)
    
    janela=CadastroIndiVw(controller)
    # janela = CadastroView(controller)
    janela.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

# from app.database.connection import engine
# from app.models.base import Base
# from app.controllers.genealogia_controller import GenealogiaController
# from app.views.main_window import MainWindow

# def main():
#     # 1. Garante que as tabelas existem
#     Base.metadata.create_all(engine)

#     # 2. Inicia o Controller
#     controller = GenealogiaController()

#     # 3. Inicia e roda a View passando o Controller
#     app = MainWindow(controller)
#     app.mainloop()

# if __name__ == "__main__":
#     main()

# from app.controllers.individuo_controller import IndividuoController
# from app.views.cadastro_view import CadastroView


# from PySide6.QtWidgets import QApplication
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.models.base import Base
# # Importar os modelos é necessário para o create_all funcionar
# from app.models.individuo import Individuo 
# from app.models.evento import Evento