# backend/scraping/city_data_sidra_to_csv.py
import json
import pandas as pd

from pathlib import Path

from utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).parent.parent
JSON_PATH = BASE_DIR / "data" / "processed" / "city_data_sidra.json"
CSV_PATH = BASE_DIR / "data" / "processed" / "city_data_sidra_microdadosedu.csv"

def run():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
        logger.info(f"📄 JSON carregado com sucesso: {JSON_PATH}")

        niveis = ["infantil", "fundamental", "medio", "eja", "especial", "tecnico"]
        linhas = []

        for uf, cidades in dados.items():
            for nome_cidade, info in cidades.items():
                linha = {
                    "estado": uf,
                    "cidade": nome_cidade,
                    "codigo_ibge": info.get("codigo_ibge"),
                    "populacao": info.get("populacao", {}).get("valor", 0),
                    "ano_populacao": info.get("populacao", {}).get("ano", 0),
                    "pib_per_capita": info.get("pib_per_capita", {}).get("valor", 0),
                    "ano_pib": info.get("pib_per_capita", {}).get("ano", 0),
                }

                educacao = info.get("educacao", {})
                linha["ano_educacao"] = educacao.get("ano", 0)

                for nivel in niveis:
                    linha[f"matriculas_{nivel}"] = educacao.get("matriculas", {}).get(nivel, 0)
                    linha[f"turmas_{nivel}"] = educacao.get("turmas", {}).get(nivel, 0)
                    linha[f"docentes_{nivel}"] = educacao.get("docentes", {}).get(nivel, 0)
                    linha[f"escolas_{nivel}"] = educacao.get("escolas", {}).get(nivel, 0)

                infra = educacao.get("infraestrutura_ensino_basico", {})
                for campo in [
                    "biblioteca", "lab_ciencias", "lab_informatica",
                    "cozinha", "refeitorio", "quadra_esportes",
                    "internet", "acessibilidade_rampas"
                ]:
                    linha[f"infra_basica_{campo}"] = infra.get(campo, 0)

                profs = educacao.get("profissionais_ensino_basico", {})
                for campo in ["professores_pedagogia", "coordenadores", "monitores"]:
                    linha[f"prof_basica_{campo}"] = profs.get(campo, 0)

                linha["cursos_tecnicos_ofertados"] = educacao.get("cursos_tecnicos_ofertados", 0)

                linhas.append(linha)

        logger.info(f"✅ Total de cidades processadas: {len(linhas)}")

        df = pd.DataFrame(linhas)

        for col in df.columns:
            if col not in ["estado", "cidade"]:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        df.to_csv(CSV_PATH, sep=";", encoding="utf-8", index=False)
        logger.info(f"📁 CSV final salvo com sucesso em: {CSV_PATH}")

    except Exception as e:
        logger.error(f"❌ Erro ao gerar CSV do SIDRA: {e}")
