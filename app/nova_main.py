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