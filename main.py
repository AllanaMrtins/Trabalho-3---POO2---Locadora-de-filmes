import sys
from PySide6.QtWidgets import QApplication
from janela_principal import JanelaPrincipal


def main():
    app = QApplication(sys.argv)

    janela = JanelaPrincipal()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()