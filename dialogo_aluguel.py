from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDialogButtonBox
)


class DialogoAluguel(QDialog):

    def __init__(self, filme, parent=None):
        super().__init__(parent)

        self.filme = filme

        self.setWindowTitle("Alugar Filme")
        self.resize(400, 300)

        layout_principal = QVBoxLayout(self)

        titulo = QLabel("Dados do aluguel")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")

        layout_principal.addWidget(titulo)

        formulario = QFormLayout()

        self.campo_cliente = QLineEdit()
        self.campo_cliente.setPlaceholderText("Digite o nome do cliente")

        self.campo_dias = QSpinBox()
        self.campo_dias.setRange(1, 30)
        self.campo_dias.setValue(1)

        formulario.addRow("Filme:", QLabel(self.filme.titulo))
        formulario.addRow("Cliente:", self.campo_cliente)
        formulario.addRow("Dias:", self.campo_dias)

        layout_principal.addLayout(formulario)
        layout_principal.addStretch()

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        botoes.accepted.connect(self.validar)
        botoes.rejected.connect(self.reject)

        layout_principal.addWidget(botoes)

    def validar(self):
        cliente = self.campo_cliente.text().strip()

        if cliente == "":
            self.campo_cliente.setFocus()
            return

        self.accept()

    def obter_dados(self):
        return self.campo_cliente.text().strip(), self.campo_dias.value()