from sqlalchemy import Column, Integer, ForeignKey, Table, String
from sqlalchemy.orm import relationship

from database import Base
from models.libros_autores import libros_autores

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    nacionalidad = Column(String, nullable=False)
    fecha_nacimiento = Column(String, nullable=False)
    fecha_fallecimiento = Column(String, nullable=True)
    biografia = Column(String, nullable=False)
    imagen = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=True)

    libros = relationship('Libro', secondary='libros_autores', back_populates='autores')

