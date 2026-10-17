import re


def converter_valor_centavos(texto):
    texto = texto.strip()

    if not re.fullmatch(r"[0-9]+([,.][0-9]{1,2})?", texto):
        raise ValueError(
            "Informe um valor positivo ou zero, "
            "com até duas casas decimais. Exemplo: 150,50."
        )

    partes = texto.replace(",", ".").split(".")
    reais = partes[0].lstrip("0") or "0"
    centavos = partes[1].ljust(2, "0") if len(partes) == 2 else "00"

    if len(reais) > 17:
        raise ValueError("O valor informado é muito alto.")

    total = int(reais) * 100 + int(centavos)

    if total > 9223372036854775807:
        raise ValueError("O valor informado é muito alto.")

    return total