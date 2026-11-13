from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QDialogButtonBox,
    QLabel
)


class DialogoFilme(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Adicionar Filme")
        self.resize(400, 300)

        layout_principal = QVBoxLayout(self)

        titulo = QLabel("Cadastrar novo filme")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")

        layout_principal.addWidget(titulo)

        formulario = QFormLayout()

        self.campo_titulo = QLineEdit()
        self.campo_titulo.setPlaceholderText("Digite o título do filme")

        self.campo_genero = QComboBox()
        self.campo_genero.addItems([
            "Ação",
            "Animação",
            "Comédia",
            "Drama",
            "Ficção",
            "Terror"
        ])

        self.campo_ano = QSpinBox()
        self.campo_ano.setRange(1900, 2100)
        self.campo_ano.setValue(2026)

        formulario.addRow("Título:", self.campo_titulo)
        formulario.addRow("Gênero:", self.campo_genero)
        formulario.addRow("Ano:", self.campo_ano)

        layout_principal.addLayout(formulario)
        layout_principal.addStretch()

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        botoes.accepted.connect(self.validar)
        botoes.rejected.connect(self.reject)

        layout_principal.addWidget(botoes)

    def validar(self):
        titulo = self.campo_titulo.text().strip()

        if titulo == "":
            self.campo_titulo.setFocus()
            return

        self.accept()

    def obter_dados(self):
        return self.campo_titulo.text().strip(), self.campo_genero.currentText(), self.campo_ano.value()