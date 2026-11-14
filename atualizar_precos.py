import os
import json
import re
import pypdf

pdf_path = "pdfs/fornecedor.pdf"
json_path = "produtos.json"

print("--- Iniciando leitura do PDF do fornecedor ---")

if not os.path.exists(pdf_path):
    print("Aviso: Nenhum PDF encontrado na pasta pdfs/")
    exit()

# 1. Lê todo o texto de todas as páginas do PDF
reader = pypdf.PdfReader(pdf_path)
texto_completo = ""
for i, page in enumerate(reader.pages):
    texto_pagina = page.extract_text()
    if texto_pagina:
        texto_completo += texto_pagina + "\n"

print(f"PDF lido com sucesso! Total de páginas: {len(reader.pages)}")

# 2. Carrega o banco de dados atual (produtos.json) para podermos atualizar os preços
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        produtos_db = json.load(f)
else:
    print("Aviso: produtos.json não encontrado. Criando base vazia.")
    produtos_db = []

# 3. Lógica de atualização inteligente baseada no texto do PDF
# Exemplo: O script varre o texto procurando correspondências com os produtos já cadastrados
alteracoes_feitas = False

for prod in produtos_db:
    nome_produto = prod['nome'].lower()
    
    # Cria uma expressão regular para procurar o nome do produto e um valor em dinheiro (ex: R$ 15,00 ou 15.00) no texto do PDF
    # Isso busca flexivelmente por números com vírgula ou ponto após o nome do item
    padrao = re.escape(nome_produto) + r'.*?(?:R\$\s*)?(\d+[\.,]\d{2})'
    resultado = re.search(padrao, texto_completo.lower(), re.IGNORECASE)
    
    if resultado:
        preco_str = resultado.group(1).replace(',', '.')
        novo_preco = float(preco_str)
        
        if prod['preco'] != novo_preco:
            print(f"Atualizando preço de '{prod['nome']}': R$ {prod['preco']} -> R$ {novo_preco}")
            prod['preco'] = novo_preco
            alteracoes_feitas = True

# 4. Salva as alterações de volta no produtos.json se houver mudanças
if alteracoes_feitas:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(produtos_db, f, ensure_ascii=False, indent=2)
    print("Banco de dados (produtos.json) atualizado com sucesso!")
else:
    print("Nenhuma alteração de preço detectada no PDF em relação aos produtos atuais.")
