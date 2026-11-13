import os

import psycopg
from psycopg.rows import dict_row


def ler_configuracao():
    """Lê os dados de conexão das variáveis de ambiente (ou do arquivo .env)."""
    carregar_env()

    return {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": int(os.environ.get("POSTGRES_PORT", "5432")),
        "dbname": os.environ.get("POSTGRES_DB", "locadora"),
        "user": os.environ.get("POSTGRES_USER", "locadora"),
        "password": os.environ.get("POSTGRES_PASSWORD", "locadora123"),
    }


def carregar_env(caminho=".env"):
    """Carrega pares CHAVE=VALOR de um .env simples, sem sobrescrever o ambiente."""
    if not os.path.exists(caminho):
        return

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if not linha or linha.startswith("#") or "=" not in linha:
                continue

            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip())


class RepositorioFilmes:
    """Camada de acesso ao banco: é a única classe que conhece SQL."""

    COLUNAS = "id, titulo, genero, ano, disponivel, cliente, dias"

    def __init__(self, configuracao=None):
        self.configuracao = configuracao or ler_configuracao()
        self.conexao = None

    def conectar(self):
        self.conexao = psycopg.connect(
            **self.configuracao,
            row_factory=dict_row,
            connect_timeout=5
        )

    def fechar(self):
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None

    def listar(self):
        with self.conexao.cursor() as cursor:
            cursor.execute(
                f"SELECT {self.COLUNAS} FROM filmes ORDER BY id"
            )
            return cursor.fetchall()

    def inserir(self, dados):
        with self.conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO filmes (titulo, genero, ano) "
                "VALUES (%s, %s, %s) RETURNING id",
                (dados["titulo"], dados["genero"], dados["ano"])
            )
            novo_id = cursor.fetchone()["id"]

        self.conexao.commit()
        return novo_id

    def atualizar_aluguel(self, id_filme, disponivel, cliente, dias):
        with self.conexao.cursor() as cursor:
            cursor.execute(
                "UPDATE filmes SET disponivel = %s, cliente = %s, dias = %s "
                "WHERE id = %s",
                (disponivel, cliente, dias, id_filme)
            )
            alteradas = cursor.rowcount

        self.conexao.commit()
        return alteradas

    def remover(self, id_filme):
        with self.conexao.cursor() as cursor:
            cursor.execute("DELETE FROM filmes WHERE id = %s", (id_filme,))
            removidas = cursor.rowcount

        self.conexao.commit()
        return removidas

    def desfazer(self):
        """Cancela a transação atual após um erro."""
        if self.conexao is not None:
            self.conexao.rollback()
