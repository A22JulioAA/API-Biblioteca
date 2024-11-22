from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base

class Prestamo(Base):
    __tablename__ = 'prestamos'
    id = Column(Integer, primary_key=True, index=True)
    fecha_prestamo = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=False)

    usuario_id = Column(Integer, ForeignKey('users.id'))
    usuario = relationship("User", back_populates="prestamos")

    libros = relationship("Libro", secondary="prestamo_libro", back_populates="prestamos")