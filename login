# main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

# Configuración de la Base de Datos (PostgreSQL)
DATABASE_URL = "postgresql://user:password@localhost/dbname"
database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelo de Usuario
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Inicializar la Base de Datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de la Autenticación JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Funciones de Hashing y Verificación de Contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funciones Auxiliares
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear un usuario por defecto
def create_default_user(db: Session):
    hashed_password = pwd_context.hash("admin")
    db_user = User(username="admin", hashed_password=hashed_password)
    db.add(db_user)
    db.commit()

# Evento de inicio de la aplicación
@app.lifespan("startup")
def startup_event():
    db = SessionLocal()
    create_default_user(db)
    db.close()

# Rutas de Autenticación
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Aquí verificarías las credenciales y autenticarías al usuario
    # (normalmente comparando con la información almacenada en la base de datos)
    # Por simplicidad, este es un ejemplo básico.
    user = {"username": form_data.username}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Función para Crear un Token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
