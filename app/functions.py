# Archivo para funciones varias

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from schemas.libro_schemas import LibroResponse

def generar_pdf(libros: list[LibroResponse], file_path: str):
    c = canvas.Canvas(file_path, pagesize=letter)

    c.setTitle("Listado de libros")
    c.setAuthor("Julio Acuña")

    c.drawString(100, 800, "Listado de libros")

    c.save()