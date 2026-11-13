from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton
)


class JanelaSobre(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Sobre")
        self.resize(400, 230)

        layout = QVBoxLayout(self)

        titulo = QLabel("Locadora de Filmes")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")

        descricao = QLabel(
            "Sistema desenvolvido para o gerenciamento de uma locadora de filmes.\n\n"
            "Interface gráfica desenvolvida com PySide6."
        )

        descricao.setWordWrap(True)

        botao_fechar = QPushButton("Fechar")
        botao_fechar.clicked.connect(self.close)

        layout.addWidget(titulo)
        layout.addWidget(descricao)
        layout.addStretch()
        layout.addWidget(botao_fechar)