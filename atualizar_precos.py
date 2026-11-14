import os
import json
import pypdf

# Caminho onde o PDF do fornecedor está salvo
pdf_path = "pdfs/fornecedor.pdf"
json_path = "produtos.json"

print("Lendo o PDF do fornecedor...")

# Verifica se o PDF existe
if not os.path.exists(pdf_path):
    print("Aviso: Nenhum PDF encontrado na pasta pdfs/")
    exit()

# Lê o conteúdo de texto do PDF
reader = pypdf.PdfReader(pdf_path)
texto_pdf = ""
for page in reader.pages:
    texto_pdf += page.extract_text() + "\n"

print("PDF lido com sucesso! O ambiente de automação está pronto.")
