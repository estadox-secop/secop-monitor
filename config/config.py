import os

# API
API_URL = "https://www.datos.gov.co/resource/p6dx-8zbt.json"
LIMITE_PROCESOS = 500
DIAS_HACIA_ATRAS = 7
INTENTOS_API = 3
ESPERA_ENTRE_INTENTOS = 10  # segundos; se multiplica por el número de intento

# Filtros
ESTADOS_ACTIVOS = [
    "Presentación de oferta",
    "Fase de ofertas",
    "Presentación de observaciones",
]

KEYWORDS = [
    ("inteligencia artificial", 10),
    ("machine learning", 10),
    ("aprendizaje automático", 10),
    ("modelo de lenguaje", 10),
    ("llm", 10),
    ("ia generativa", 10),
    ("deep learning", 10),
    ("interoperabilidad", 8),
    ("transformación digital", 8),
    ("gobierno digital", 8),
    ("govtech", 8),
    ("automatización", 6),
    ("analítica de datos", 6),
    ("ciencia de datos", 6),
    ("expediente electrónico", 5),
    ("desarrollo web", 5),
    ("aplicación web", 5),
    ("ciberseguridad", 5),
    ("plataforma digital", 5),
    ("big data", 5),
    ("gestión documental", 4),
    ("software", 4),
    ("tecnología", 2),
    ("tecnologia", 2),
    ("sistemas de información", 2),
    ("infraestructura tecnológica", 2),
    ("soporte técnico", 2),
]

# Email
# Los destinatarios no viven en el codigo: el repositorio es publico y los
# correos quedarian expuestos a robots de spam. Se leen del entorno, separados
# por comas (en GitHub Actions llegan desde el secret EMAIL_DESTINATARIOS).
EMAIL_DESTINATARIOS = [
    c.strip() for c in os.environ.get("EMAIL_DESTINATARIOS", "").split(",") if c.strip()
]
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
