import unittest

from validacoes import converter_valor_centavos


class TestValidacoes(unittest.TestCase):
    def test_valores_validos(self):
        casos = {
            "150,50": 15050,
            "150.50": 15050,
            "150": 15000,
            "0": 0,
            "0,01": 1,
            " 25,5 ": 2550,
            "92233720368547758,07": 9223372036854775807,
        }

        for entrada, esperado in casos.items():
            with self.subTest(entrada=entrada):
                self.assertEqual(
                    converter_valor_centavos(entrada),
                    esperado
                )

    def test_valores_invalidos(self):
        casos = [
            "",
            "abc",
            "-10",
            "1,001",
            "1e999999999",
            "NaN",
            "Infinity",
            "92233720368547758,08",
        ]

        for entrada in casos:
            with self.subTest(entrada=entrada):
                with self.assertRaises(ValueError):
                    converter_valor_centavos(entrada)


if __name__ == "__main__":
    unittest.main()