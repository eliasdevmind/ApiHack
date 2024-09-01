from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter variáveis de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

if not all([DATABASE_URL, SECRET_KEY]):
    raise ValueError("Por favor, defina todas as variáveis de ambiente: DATABASE_URL e SECRET_KEY")

# Configuração do banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição dos modelos
class Estacao(Base):
    __tablename__ = "estacoes"

    id = Column(Integer, primary_key=True, index=True)
    localizacao = Column(Text, nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    cep = Column(String(10), nullable=False)
    iframe_mapa = Column(Text, nullable=True)
    fotos = Column(String)  # URL da imagem armazenada como string
    contatos = Column(Text)
    cursos = relationship("EstacaoCurso", back_populates="estacao")

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)  # Nome único do curso
    descricao = Column(Text)
    carga_horaria = Column(Integer, nullable=False)
    nome_professor = Column(String(100), nullable=True)  # Nome do professor não obrigatório

class EstacaoCurso(Base):
    __tablename__ = "estacoes_cursos"

    estacao_id = Column(Integer, ForeignKey("estacoes.id", ondelete="CASCADE"), primary_key=True)
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), primary_key=True)
    estacao = relationship("Estacao", back_populates="cursos")
    curso = relationship("Curso")

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar o aplicativo FastAPI
app = FastAPI()

# Configuração do CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos Pydantic
class EstacaoCreate(BaseModel):
    localizacao: str
    nome: str
    descricao: Optional[str] = None
    cep: str
    iframe_mapa: Optional[str] = None
    fotos: Optional[HttpUrl] = None  # URL da imagem
    contatos: Optional[str] = None

class CursoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    carga_horaria: int
    nome_professor: Optional[str] = None  # Nome do professor não obrigatório

# Endpoint para criar uma nova estação
@app.post("/estacoes/", response_model=EstacaoCreate)
def create_estacao(estacao: EstacaoCreate, db: Session = Depends(get_db)):
    nova_estacao = Estacao(
        localizacao=estacao.localizacao,
        nome=estacao.nome,
        descricao=estacao.descricao,
        cep=estacao.cep,
        iframe_mapa=estacao.iframe_mapa,
        fotos=estacao.fotos,
        contatos=estacao.contatos
    )
    db.add(nova_estacao)
    db.commit()
    db.refresh(nova_estacao)
    return nova_estacao

# Endpoint para criar um novo curso
@app.post("/cursos/", response_model=CursoCreate)
def create_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    novo_curso = Curso(
        nome=curso.nome,
        descricao=curso.descricao,
        carga_horaria=curso.carga_horaria,
        nome_professor=curso.nome_professor
    )
    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)
    return novo_curso

# Endpoint para listar estações com filtros
@app.get("/estacoes/", response_model=List[EstacaoCreate])
def read_estacoes(
    nome: Optional[str] = None,
    cep: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Estacao)
    if nome:
        query = query.filter(Estacao.nome.ilike(f"%{nome}%"))
    if cep:
        query = query.filter(Estacao.cep == cep)
    return query.offset(skip).limit(limit).all()

# Endpoint para listar cursos com filtros
@app.get("/cursos/", response_model=List[CursoCreate])
def read_cursos(
    nome: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Curso)
    if nome:
        query = query.filter(Curso.nome.ilike(f"%{nome}%"))
    return query.offset(skip).limit(limit).all()

# Executar a aplicação FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
