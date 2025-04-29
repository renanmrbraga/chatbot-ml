#!/usr/bin/env python3
import json
import re
import csv
from pathlib import Path
from typing import Tuple

# Caminhos
BASE_DIR = Path(__file__).parent.parent  # chatbot-llm/scraper
RAW_JSON = BASE_DIR / "data" / "raw" / "city_data_sidra.json"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_CSV = PROCESSED_DIR / "municipios.csv"

# Garante que a pasta processed existe
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def parse_city_key(key: str) -> Tuple[str, str]:
    """
    Devolve (cidade, estado) a partir da chave do JSON.
    Exemplo de key: "Alta Floresta D'Oeste (RO) (População residente estimada)"
    """
    # State: última ocorrência de (XX)
    m = re.search(r"\(([A-Z]{2})\)", key)
    estado = m.group(1) if m else ""
    # Remove sufixos e o "(UF)"
    nome = key.replace(" (População residente estimada)", "")
    nome = re.sub(r" \([A-Z]{2}\)$", "", nome)
    return nome, estado


def main() -> None:
    # Carrega JSON
    with open(RAW_JSON, encoding="utf-8") as f:
        data = json.load(f)

    # Prepara as linhas do CSV
    rows = []
    for key, info in data.items():
        cidade, estado = parse_city_key(key)
        codigo = info.get("codigo_ibge")
        pop = info.get("populacao", {})
        pib = info.get("pib_per_capita", {})

        rows.append(
            {
                "Estado": estado,
                "Cidade": cidade,
                "Código_IBGE": codigo,
                "População": pop.get("valor"),
                "Ano_População": pop.get("ano"),
                "PIB": pib.get("valor"),
                "Ano_PIB": pib.get("ano"),
            }
        )

    # Escreve CSV
    fieldnames = [
        "Estado",
        "Cidade",
        "Código_IBGE",
        "População",
        "Ano_População",
        "PIB",
        "Ano_PIB",
    ]
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV gerado em: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
