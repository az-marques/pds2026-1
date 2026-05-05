# Uma aplicação PySide6/QML consiste, principalmente, em dois arquivos diferentes: um arquivo com a descrição QML da interface do usuário e um arquivo Python que carrega o arquivo QML.

# from PySide6.QtWidgets import QApplication

import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

if __name__ == "__main__":
    app = QGuiApplication()
    view = QQuickView()
    view.engine().addImportPath(sys.path[0])
    view.loadFromModule("App", "Main")
    view.show()
    ex = app.exec()
    del view
    sys.exit(ex)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# # Importamos a Base de app.models para que o SQLAlchemy conheça as tabelas
# from app.models import Base 

# # URL do banco de dados (pode ser movida para um .env futuramente)
# DATABASE_URL = "sqlite:///banco_genealogia.db"

# # 1. Cria o motor de conexão
# engine = create_engine(DATABASE_URL, echo=True)

# # 2. Cria a fábrica de sessões (usada pelo Controller)
# SessionLocal = sessionmaker(bind=engine)

# def init_db():
#     """
#     Cria todas as tabelas no banco de dados se elas ainda não existirem.
#     """
#     # Base.metadata.create_all utiliza as definições em app/models/individuo.py
#     Base.metadata.create_all(engine)