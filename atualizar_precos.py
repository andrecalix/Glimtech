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

# 3. Lógica de atualização baseada no texto do PDF
alteracoes_feitas = False
texto_lower = texto_completo.lower()

for prod in produtos_db:
    nome_produto = prod['nome'].lower()
    preco_atual = float(prod.get('preco') or 0.0)

    # Procura o nome do produto e um valor monetário na mesma linha (sem atravessar quebras de linha)
    padrao = re.escape(nome_produto) + r'[^\n]*?(?:r\$\s*)?(\d+[\.,]\d{2})'
    resultado = re.search(padrao, texto_lower)

    if resultado:
        preco_str = resultado.group(1).replace(',', '.')
        novo_preco = float(preco_str)
    else:
        # Se não houver preço no PDF para este item, limpa/zera o valor
        novo_preco = 0.0

    if preco_atual != novo_preco:
        print(f"Atualizando preço de '{prod['nome']}': R$ {preco_atual:.2f} -> R$ {novo_preco:.2f}")
        prod['preco'] = novo_preco
        alteracoes_feitas = True

# 4. Salva as alterações de volta no produtos.json se houver mudanças
if alteracoes_feitas:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(produtos_db, f, ensure_ascii=False, indent=2)
    print("Banco de dados (produtos.json) atualizado com sucesso!")
else:
    print("Nenhuma alteração de preço detectada no PDF em relação aos produtos atuais.")
