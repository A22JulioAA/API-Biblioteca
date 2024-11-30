from sqlalchemy import Column, Integer, String, ForeignKey, Table

from database import Base

libros_generos = Table(
    'libros_generos',
    Base.metadata,
    Column('libro_id', Integer, ForeignKey('libros.id'), primary_key=True),
    Column('genero_id', Integer, ForeignKey('generos.id'), primary_key=True)
)