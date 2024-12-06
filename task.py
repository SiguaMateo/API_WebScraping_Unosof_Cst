from apscheduler.schedulers.background import BackgroundScheduler
from src.main import scrape_data
from src.manage_data import save
import logging
import time

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def retry_on_failure(func, retries=3, delay=5):
    """
    Función para intentar ejecutar una tarea con reintentos.
    :param func: Función a ejecutar
    :param retries: Número máximo de intentos
    :param delay: Tiempo de espera entre reintentos (en segundos)
    """
    for attempt in range(retries):
        try:
            func()
            return  # Salir si la tarea se ejecuta correctamente
        except Exception as e:
            logging.error(f"Error en intento {attempt + 1}: {e}")
            time.sleep(delay)
    logging.error(f"Función {func.__name__} falló tras {retries} intentos.")


def get_data_task():
    """
    Función que ejecuta el web scraping con reintentos.
    """
    logging.info("Iniciando tarea de extracción de datos...")
    retry_on_failure(lambda: (scrape_data(), save()))
    logging.info("Tarea de extracción finalizada.")


def start_scheduler():
    """
    Inicia un programador para ejecutar la tarea programada diariamente a las 23:00.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_data_task, "cron", hour=10, minute=30)  # Ejecutar a las 23:00
    scheduler.start()
    logging.info("Scheduler iniciado. La tarea se ejecutará diariamente a las 23:00.")
