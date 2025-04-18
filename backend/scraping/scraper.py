# backend/scraping/scraper.py
from utils.logger import get_logger
from scraping.scraper_sidra_ibge import run as run_sidra
from scraping.extrator_basico_microdados import run as run_basico
from scraping.extrator_tecnico_microdados import run as run_tecnico
from scraping.city_data_sidra_to_csv import run as run_to_csv
from scraping.insert_database import run as run_insert

logger = get_logger(__name__)

def main():
    logger.info("🚀 Iniciando pipeline de scraping completo...")

    etapas = [
        ("🔍 Etapa 1: Coleta do SIDRA (IBGE)", run_sidra),
        ("📚 Etapa 2: Extração de microdados educacionais (básico)", run_basico),
        ("🛠️ Etapa 3: Extração de dados técnicos", run_tecnico),
        ("📄 Etapa 4: Geração do CSV final", run_to_csv),
        ("📥 Etapa 5: Inserção no banco de dados", run_insert),
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
