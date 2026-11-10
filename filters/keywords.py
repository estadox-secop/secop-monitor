import sys, os
from datetime import date, datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import KEYWORDS


def esta_vigente(proceso):
    crudo = proceso.get("fecha_de_recepcion_de")
    if not crudo:
        return True
    fecha_limite = datetime.fromisoformat(crudo.replace("Z", "+00:00")).date()
    return fecha_limite >= date.today()


def get_prioridad(puntaje):
    if puntaje >= 15:
        return "MUY ALTA"
    elif puntaje >= 10:
        return "ALTA"
    elif puntaje >= 5:
        return "MEDIA"
    else:
        return "BAJA"


def calcular_puntaje(proceso):
    texto = " ".join([
        proceso.get("nombre_del_procedimiento", ""),
        proceso.get("descripci_n_del_procedimiento", ""),
    ]).lower()

    puntaje = 0
    coincidencias = []
    for keyword, peso in KEYWORDS:
        if keyword in texto:
            puntaje += peso
            coincidencias.append(keyword)

    return puntaje, coincidencias


def filtrar_y_ordenar(procesos):
    resultados = []
    for p in procesos:
        puntaje, coincidencias = calcular_puntaje(p)
        if puntaje > 0 and esta_vigente(p):
            resultados.append({
                "proceso": p,
                "puntaje": puntaje,
                "prioridad": get_prioridad(puntaje),
                "coincidencias": coincidencias,
            })
    return sorted(resultados, key=lambda x: x["puntaje"], reverse=True)