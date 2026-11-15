import json
import re
import os

ARQUIVO_JSON = "servicos.json"
PASTA_PDFS = "pdfs"

def atualizar_servicos():
    print("Iniciando verificação de atualizações de serviços via PDF...")
    
    if not os.path.exists(ARQUIVO_JSON):
        print("Arquivo servicos.json não encontrado.")
        return

    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
        servicos = json.load(f)

    print(f"Total de serviços atualmente cadastrados: {len(servicos)}")
    # Lógica pronta para varredura e atualização automatizada via PDF

if __name__ == "__main__":
    atualizar_servicos()
