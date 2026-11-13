class Filme:
    def __init__(self, titulo, genero, ano, id=None):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.disponivel = True
        self.cliente = ""
        self.dias = 0

    def __str__(self):
        if self.disponivel:
            status = "Disponível"
        else:
            status = "Alugado"

        return f"{self.titulo} | {self.genero} | {self.ano} | {status}"

    def para_dicionario(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "ano": self.ano,
            "disponivel": self.disponivel,
            "cliente": self.cliente,
            "dias": self.dias
        }

    @classmethod
    def de_dicionario(cls, dados):
        filme = cls(
            dados["titulo"],
            dados["genero"],
            dados["ano"],
            dados.get("id")
        )

        filme.disponivel = dados["disponivel"]
        filme.cliente = dados["cliente"]
        filme.dias = dados["dias"]

        return filme
