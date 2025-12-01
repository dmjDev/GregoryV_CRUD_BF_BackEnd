import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

##LOCAL##
# Parámetros de conexión de forma local con un BackEnd en un entorno virtual (revisar .env)
DB_HOST = os.getenv('DB_HOST', default=None)
DB_PORT_LOCAL = os.getenv('DB_PORT_LOCAL', default=None)  # COMENTAMOS ESTA LÍNEA AL CONECTAR MEDIANTE LOS CONTENEDORES
DB_USER = os.getenv('DB_USER', default=None)
DB_PASSWORD = os.getenv('DB_PASSWORD', default=None)
DB_NAME = os.getenv('DB_NAME', default=None)
DB_DIALECT = os.getenv('DB_DIALECT', default=None)
DATABASE_URL = (
    f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT_LOCAL}/{DB_NAME}"
)

##DOCKER##
# Parámetros de conexión con contenedor BackEnd (revisar .env)
# DB_HOST = os.getenv('DB_HOST', default=None)
# DB_USER = os.getenv('DB_USER', default=None)
# DB_PASSWORD = os.getenv('DB_PASSWORD', default=None)
# DB_NAME = os.getenv('DB_NAME', default=None)
# DB_DIALECT = os.getenv('DB_DIALECT', default=None)
# DATABASE_URL = (
#     f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# )

# Intentar crear el motor de SQLAlchemy con reintentos
max_retries = 5
engine = None

for attempt in range(max_retries):
    try:
        # Crea el motor de la base de datos
        # echo=True mostrará las consultas SQL generadas por SQLAlchemy en la consola (útil para depurar)
        engine = create_engine(DATABASE_URL, echo=True)
        
        # Intentar conectar inmediatamente para verificar que funciona
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos MySQL usando SQLAlchemy.")
            # Opcional: ejecutar una consulta simple para probar
            result = connection.execute(text("SELECT 1"))
            print(f"Resultado de la prueba: {result.scalar()}")
        break
    
    except Exception as e:
        if attempt < max_retries - 1:
            print(f"Error de conexión: {e}. Reintentando en 5 segundos... (Intento {attempt + 1}/{max_retries})")
            time.sleep(5)
        else:
            print(f"Error de conexión persistente. No se pudo conectar a la base de datos.")
            raise

# A partir de aquí puedes usar 'engine' para todas tus operaciones de SQLAlchemy
# Por ejemplo, para crear sesiones ORM o ejecutar más consultas.


localSession = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
Base = declarative_base()