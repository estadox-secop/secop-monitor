import requests
import sys, os, time
from datetime import date, timedelta
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import (
    API_URL,
    LIMITE_PROCESOS,
    ESTADOS_ACTIVOS,
    DIAS_HACIA_ATRAS,
    INTENTOS_API,
    ESPERA_ENTRE_INTENTOS,
)

def obtener_procesos():
    # Construir filtro de estados con SoQL
    estados_filtro = " OR ".join(
        [f"estado_resumen='{e}'" for e in ESTADOS_ACTIVOS]
    )

    # El filtro de estados por sí solo matchea millones de registros históricos
    # (no solo los activos hoy), así que se acota a los últimos días. También
    # evita el problema de que id_del_proceso se ordena como texto, no número:
    # un ID de 8 dígitos ("10347391") queda por detrás de uno de 7 ("9999999")
    # en un ORDER BY DESC, así que ordenar por fecha real es lo correcto.
    desde = (date.today() - timedelta(days=DIAS_HACIA_ATRAS)).isoformat()
    where = (
        f"({estados_filtro}) "
        f"AND fecha_de_publicacion_del >= '{desde}' "
        "AND fecha_de_publicacion_del IS NOT NULL"
    )

    params = {
        "$limit": LIMITE_PROCESOS,
        "$where": where,
        "$order": "fecha_de_publicacion_del DESC",
    }

    # datos.gov.co se cae o devuelve 5xx de vez en cuando. Sin reintentos, un
    # hipo de unos segundos tumbaba el run completo y ese día no llegaba correo.
    ultimo_error = None
    for intento in range(1, INTENTOS_API + 1):
        try:
            response = requests.get(API_URL, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            ultimo_error = e
            print(f"Intento {intento}/{INTENTOS_API} falló al consultar la API: {e}")
            if intento < INTENTOS_API:
                time.sleep(ESPERA_ENTRE_INTENTOS * intento)

    raise RuntimeError(
        f"La API de SECOP no respondió tras {INTENTOS_API} intentos: {ultimo_error}"
    )