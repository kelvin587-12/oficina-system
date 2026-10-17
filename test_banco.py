import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from banco import salvar_ordem_banco
from validacoes import converter_valor_centavos


class TestIntegracaoBanco(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.banco = Path(self.pasta.name) / "teste.db"

        with closing(sqlite3.connect(self.banco)) as conexao:
            with conexao:
                conexao.executescript("""
                    CREATE TABLE veiculos (
                        id INTEGER PRIMARY KEY
                    );

                    CREATE TABLE ordens_servico (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        veiculo_id INTEGER NOT NULL,
                        descricao TEXT NOT NULL,
                        valor_centavos INTEGER NOT NULL
                            CHECK (valor_centavos >= 0),
                        status TEXT NOT NULL CHECK (
                            status IN (
                                'Aberta', 'Em andamento', 'Concluída'
                            )
                        ),
                        FOREIGN KEY (veiculo_id)
                            REFERENCES veiculos(id)
                    );

                    INSERT INTO veiculos (id) VALUES (1);
                """)

    def consultar_ordens(self):
        with closing(sqlite3.connect(self.banco)) as conexao:
            return conexao.execute("""
                SELECT id, veiculo_id, descricao,
                       valor_centavos, status
                FROM ordens_servico
            """).fetchall()

    def test_grava_e_persiste_ordem(self):
        valor = converter_valor_centavos("150,50")

        numero = salvar_ordem_banco(
            self.banco, 1, "Troca de óleo", valor, "Aberta"
        )

        self.assertEqual(
            self.consultar_ordens(),
            [(numero, 1, "Troca de óleo", 15050, "Aberta")]
        )

    def test_rejeita_veiculo_inexistente(self):
        with self.assertRaises(sqlite3.IntegrityError):
            salvar_ordem_banco(
                self.banco, 999, "Teste", 1000, "Aberta"
            )

        self.assertEqual(self.consultar_ordens(), [])

    def test_rejeita_status_invalido(self):
        with self.assertRaises(sqlite3.IntegrityError):
            salvar_ordem_banco(
                self.banco, 1, "Teste", 1000, "Inválido"
            )

        self.assertEqual(self.consultar_ordens(), [])

    def test_rejeita_valor_negativo(self):
        with self.assertRaises(sqlite3.IntegrityError):
            salvar_ordem_banco(
                self.banco, 1, "Teste", -100, "Aberta"
            )

        self.assertEqual(self.consultar_ordens(), [])


if __name__ == "__main__":
    unittest.main()