import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(__file__))

from monitor.secop_client import obtener_procesos
from filters.keywords import filtrar_y_ordenar
from database.tracker import inicializar, filtrar_nuevos, marcar_todos_vistos
from notifications.email_service import enviar_alerta, enviar_sin_novedades
from config.config import EMAIL_DESTINATARIOS


def correr_monitor():
    if not EMAIL_DESTINATARIOS:
        raise RuntimeError(
            "No hay destinatarios: define EMAIL_DESTINATARIOS (separados por comas) "
            "como variable de entorno. En GitHub Actions viene del secret del mismo nombre."
        )

    inicializar()

    print("Consultando SECOP II...")
    procesos = obtener_procesos()
    print(f"Obtenidos  : {len(procesos)}")

    relevantes = filtrar_y_ordenar(procesos)
    print(f"Relevantes : {len(relevantes)}")

    nuevos = filtrar_nuevos([r["proceso"] for r in relevantes])
    print(f"Nuevos     : {len(nuevos)}")

    if not nuevos:
        print("\nSin procesos nuevos.")
        try:
            enviar_sin_novedades(EMAIL_DESTINATARIOS, len(relevantes))
            print(f"Correo (sin novedades) enviado a {len(EMAIL_DESTINATARIOS)} destinatarios.")
        except Exception as e:
            print(f"ERROR enviando correo: {e}")
        return

    ids_nuevos = {p.get("id_del_proceso") for p in nuevos}
    nuevos_con_puntaje = [r for r in relevantes if r["proceso"].get("id_del_proceso") in ids_nuevos]

    print("\n=== PROCESOS NUEVOS ===")
    for r in nuevos_con_puntaje:
        p = r["proceso"]
        print("---")
        print(f"Prioridad     : {r['prioridad']}")
        print(f"Coincidencias : {', '.join(r['coincidencias'])}")
        print(f"Entidad       : {p.get('entidad')}")
        print(f"Estado        : {p.get('estado_resumen')}")
        print(f"Desc          : {p.get('descripci_n_del_procedimiento', '')[:120]}")
        print(f"Valor         : ${int(p.get('precio_base') or 0):,}")
        print(f"Cierre        : {p.get('fecha_de_recepcion_de') or 'Sin fecha'}")
        print(f"URL           : {p.get('urlproceso', {}).get('url')}")

    try:
        enviar_alerta(nuevos_con_puntaje, EMAIL_DESTINATARIOS)
        print(f"\nCorreo enviado a {len(EMAIL_DESTINATARIOS)} destinatarios.")
    except Exception as e:
        print(f"\nERROR enviando correo: {e}")
        return

    marcar_todos_vistos(nuevos)
    print(f"{len(nuevos)} procesos marcados como vistos.")


if __name__ == "__main__":
    correr_monitor()