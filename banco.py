import sqlite3
from contextlib import closing


def salvar_ordem_banco(
    caminho_banco,
    veiculo_id,
    descricao,
    valor_centavos,
    status
):
    with closing(sqlite3.connect(caminho_banco)) as conexao:
        conexao.execute("PRAGMA foreign_keys = ON")

        with conexao:
            cursor = conexao.execute(
                """
                INSERT INTO ordens_servico (
                    veiculo_id, descricao, valor_centavos, status
                )
                VALUES (?, ?, ?, ?)
                """,
                (veiculo_id, descricao, valor_centavos, status)
            )

            return cursor.lastrowid