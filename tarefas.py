from queue import Queue

from PySide6.QtCore import QThread, Signal

from repositorio import RepositorioFilmes


class GerenciadorBanco(QThread):
    """Thread que executa as operações no banco, uma de cada vez, em ordem.

    A janela envia pedidos pela fila e recebe o resultado pelo sinal
    `resultado(operacao, dados, erro)`. A conexão é criada dentro da própria
    thread, o que evita compartilhar a conexão entre threads.
    """

    resultado = Signal(str, object, str)

    def __init__(self):
        super().__init__()
        self.fila = Queue()

    def carregar(self):
        self.fila.put(("carregar", None))

    def inserir(self, dados):
        self.fila.put(("inserir", dados))

    def atualizar_aluguel(self, id_filme, disponivel, cliente, dias):
        self.fila.put(
            ("atualizar", (id_filme, disponivel, cliente, dias))
        )

    def remover(self, id_filme):
        self.fila.put(("remover", id_filme))

    def encerrar(self):
        self.fila.put(("encerrar", None))

    def run(self):
        repositorio = RepositorioFilmes()

        while True:
            operacao, dados = self.fila.get()

            if operacao == "encerrar":
                break

            try:
                if repositorio.conexao is None:
                    repositorio.conectar()

                if operacao == "carregar":
                    saida = repositorio.listar()

                elif operacao == "inserir":
                    saida = repositorio.inserir(dados)

                elif operacao == "atualizar":
                    saida = repositorio.atualizar_aluguel(*dados)

                elif operacao == "remover":
                    saida = repositorio.remover(dados)

                self.resultado.emit(operacao, saida, "")

            except Exception as erro:
                repositorio.desfazer()
                # descarta a conexão para tentar reconectar no próximo pedido
                repositorio.fechar()
                self.resultado.emit(operacao, None, str(erro))

        repositorio.fechar()
