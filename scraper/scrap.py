# backend/scraping/scrap.py
from typing import Callable, List, Tuple
from utils.logger import get_logger
from .scraper_sidra_ibge import run as run_sidra
from .city_data_sidra_to_csv import run as run_to_csv
from .insert_database import run as run_insert

logger = get_logger(__name__)


def main() -> None:
    logger.info("🚀 Iniciando pipeline de scraping completo...")

    etapas: List[Tuple[str, Callable[[], None]]] = [
        ("🔍 Etapa 1 – Coleta do SIDRA (IBGE)", run_sidra),
        ("📄 Etapa 2 – Geração do CSV final", run_to_csv),
        ("📥 Etapa 3 – Inserção no banco (educação + técnica)", run_insert),
    ]

    for titulo, func in etapas:
        logger.info(titulo)
        try:
            func()
        except Exception as e:
            logger.critical(f"❌ Falha na etapa: {titulo} → {e}")
            logger.critical("🛑 Pipeline encerrado devido a erro crítico.")
            break
    else:
        logger.success("✅ Pipeline executado com sucesso! Dados atualizados.")


if __name__ == "__main__":
    main()
