from sqlalchemy import Column, Integer, ForeignKey, Table

from database import Base

libros_autores = Table(
    'libros_autores',
    Base.metadata,
    Column('libro_id', Integer, ForeignKey('libros.id'), primary_key=True),
    Column('autor_id', Integer, ForeignKey('autores.id'), primary_key=True)
)