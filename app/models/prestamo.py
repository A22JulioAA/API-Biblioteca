from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base
from models.prestamo_libros import prestamos_libros

class Prestamo(Base):
    __tablename__ = 'prestamos'
    id = Column(Integer, primary_key=True, index=True)
    fecha_prestamo = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=False)
    estado = Column(String, nullable=False, default='activo')

    usuario_id = Column(Integer, ForeignKey('users.id'))
    usuario = relationship("User", back_populates="prestamos")

    libros = relationship("Libro", secondary="prestamos_libros", back_populates="prestamos")