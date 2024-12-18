from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Numeric

from database import Base

class Libro(Base):
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(13), index=True, unique=True, nullable=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    editorial = Column(String, nullable=True)
    pais = Column(String, nullable=True)
    idioma = Column(String, nullable=True)
    num_paginas = Column(Integer, nullable=True)
    ano_edicion = Column(Integer, nullable=True)
    precio = Column(Numeric(10, 2), nullable=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=True)

    prestamos = relationship("Prestamo", secondary="prestamos_libros", back_populates="libros")
    autores = relationship('Autor', secondary='libros_autores', back_populates='libros')
    generos = relationship('Genero', secondary='libros_generos', back_populates='libros')