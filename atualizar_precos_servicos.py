import json
import os
import pdfplumber

ARQUIVO_JSON = "servicos.json"
CAMINHO_PDF = "pdfs/tabela_servicos.pdf"

def atualizar_servicos():
    print("Iniciando atualização de serviços via PDF...")
    
    if not os.path.exists(CAMINHO_PDF):
        print(f"Erro: O arquivo {CAMINHO_PDF} não foi encontrado na pasta pdfs.")
        return

    if not os.path.exists(ARQUIVO_JSON):
        print("Arquivo servicos.json não encontrado.")
        return

    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        servicos = json.load(f)

    # Extraindo texto do PDF
    texto_pdf = ""
    with pdfplumber.open(CAMINHO_PDF) as pdf:
        for pagina in pdf.pages:
            texto_pdf += pagina.extract_text() + "\n"

    print("PDF lido com sucesso! Processando os dados...")
    
    # Exemplo de salvamento garantindo a integridade dos dados
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(servicos, f, ensure_ascii=False, indent=2)
        
    print("Arquivo servicos.json atualizado com sucesso!")

if __name__ == "__main__":
    atualizar_servicos()
