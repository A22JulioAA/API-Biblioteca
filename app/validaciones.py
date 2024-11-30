# Se definen las funciones para validar diferentes campos.

from isbnlib import is_isbn10, is_isbn13
from fastapi import HTTPException

# Función para validar el ISBN
def validar_isbn(isbn: str):
    if not is_isbn10(isbn) and not is_isbn13(isbn):
        raise HTTPException(status_code=400, detail='El ISBN no es válido')