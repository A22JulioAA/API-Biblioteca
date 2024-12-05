# Archivo para funciones varias

from fpdf import FPDF
from fastapi.responses import FileResponse
import os


from schemas.libro_schemas import LibroResponse

def generar_pdf(libros: list[LibroResponse], file_path: str):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)

    pdf.cell(200, 10, 'Lista de libros', 0, 1, 'C')

    for libro in libros:
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 10, f'Título: {libro.titulo}', 0, 1, ln=True)
    
    pdf.output(file_path)