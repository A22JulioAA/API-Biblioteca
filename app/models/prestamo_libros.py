from sqlalchemy import Column, Integer, String, ForeignKey, Table

from database import Base

prestamos_libros = Table(
    'prestamos_libros',
    Base.metadata,
    Column('prestamo_id', Integer, ForeignKey('prestamos.id'), primary_key=True),
    Column('libro_id', Integer, ForeignKey('libros.id'), primary_key=True)
)