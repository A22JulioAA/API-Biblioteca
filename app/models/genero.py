from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from models.libros_generos import libros_generos

class Genero(Base):
    __tablename__ = 'generos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=True)

    libros = relationship('Libro', secondary='libros_generos', back_populates='generos')

