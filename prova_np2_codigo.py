"""
prova_np2_codigo.py

Script para leitura e extração de dados estruturados do documento "Prova NP2 - Catálogo de Destinos - PyTravel.docx",
organização em listas e geração de novas categorias por correlação.
"""

import time
import re
from docx import Document

def extrair_listas_por_secao(caminho_docx):
    """
    Lê o arquivo Word especificado e extrai 6 listas principais conforme seções:
      - Destinos para Cidades Praianas
      - Destinos de Cidades Capitais
      - Destinos de Cidades Interiorana
      - Pacotes de Avião
      - Pacotes de Ônibus
      - Pacotes de Navio

    Retorna um dicionário com as listas correspondentes.
    """
    doc = Document(caminho_docx)

    # Mapeamento do texto exato dos títulos para chaves internas
    titulos_secoes = {
        '🌴 Destinos para Cidades Praianas': 'praias',
        '🏙️ Destinos para Cidades Capitais': 'capitais',
        '🌄 Destinos para Cidades Interiorana': 'interior',
        '✈️ Pacotes de Avião': 'aviao',
        '🚌 Pacotes de Ônibus': 'onibus',
        '🚢 Pacotes de Navio': 'navio'
    }

    # Inicializa dicionário com listas vazias
    secoes = {
        'praias': [],
        'capitais': [],
        'interior': [],
        'aviao': [],
        'onibus': [],
        'navio': []
    }

    current_section = None       # chave atual (ex: 'praias', 'capitais', etc)
    coletando = False            # flag que indica se devemos coletar nomes de cidades

    for paragrafo in doc.paragraphs:
        texto = paragrafo.text.strip()

        # 1. Verifica se o parágrafo corresponde a um título de seção
        if texto in titulos_secoes:
            current_section = titulos_secoes[texto]
            coletando = False
            continue

        # 2. Se já identificamos a seção e ainda não começamos a coletar, 
        #    procuramos a linha que inicia com "Cidades"
        if current_section and not coletando:
            # Em Pacotes de Avião, Ônibus e Navio, o prefixo é ligeiramente diferente,
            # mas todos começam com "Cidades" em minúsculo ou maiúsculo.
            if re.match(r'^(Cidades)', texto, re.IGNORECASE):
                coletando = True
            continue

        # 3. Se estivermos no modo de coleta, registramos cada linha não vazia
        if coletando:
            # Caso encontre linha em branco, encerra coleta desta seção
            if texto == '':
                coletando = False
                current_section = None
                continue

            # Caso a linha contenha um novo título de seção, interrompe coleta
            if texto in titulos_secoes:
                coletando = False
                current_section = titulos_secoes[texto]
                continue

            # Caso contrário, adiciona o texto (nome da cidade) à lista apropriada
            secoes[current_section].append(texto)

    return secoes

def gerar_novas_categorias(listas):
    """
    Recebe um dicionário com as 6 listas principais e gera novas categorias por correlação:
      - Capitais que são cidades praianas
      - Destinos de praias com pacotes de ônibus
      - Cidades do interior com pacote de avião
      - Cidades com rotas de navio que também são capitais

    Retorna um dicionário com essas novas categorias.
    """
    # Converte cada lista principal em conjunto para facilitar interseções
    set_praias   = set(listas['praias'])
    set_capitais = set(listas['capitais'])
    set_interior = set(listas['interior'])
    set_aviao    = set(listas['aviao'])
    set_onibus   = set(listas['onibus'])
    set_navio    = set(listas['navio'])

    # 1. Capitais que são cidades praianas
    capitais_praianas = sorted(list(set_capitais & set_praias))

    # 2. Destinos de praias com pacotes de ônibus
    praias_onibus = sorted(list(set_praias & set_onibus))

    # 3. Cidades do interior com pacote de avião (caso haja)
    interior_aviao = sorted(list(set_interior & set_aviao))

    # 4. Cidades com rotas de navio que também são capitais
    capitais_navio = sorted(list(set_navio & set_capitais))

    novas = {
        'capitais_praianas': capitais_praianas,
        'praias_onibus': praias_onibus,
        'interior_aviao': interior_aviao,
        'capitais_navio': capitais_navio
    }

    return novas

def main():
    """
    Função principal:
      - Registra timestamps de cada etapa
      - Executa a extração das listas
      - Gera as novas categorias por correlação
      - Exibe resultados e tempos de execução
    """
    caminho_arquivo = 'Catálogo de Destinos - PyTravel - Prof. Sandro Mesquita.docx'

    # --- Início do cronômetro geral ---
    inicio_total = time.time()

    # Leitura e extração das listas principais
    inicio_extracao = time.time()
    listas_principais = extrair_listas_por_secao(caminho_arquivo)
    fim_extracao = time.time()

    # Geração de novas categorias (correlações)
    inicio_correlacao = time.time()
    novas_categorias = gerar_novas_categorias(listas_principais)
    fim_correlacao = time.time()

    # --- Fim do cronômetro geral ---
    fim_total = time.time()

    # Apresenta as listas principais
    print("\n--- Listas Principais Extraídas ---")
    print(f"1. Destinos para Cidades Praianas ({len(listas_principais['praias'])} itens):")
    for cidade in listas_principais['praias']:
        print(f"   - {cidade}")

    print(f"\n2. Destinos para Cidades Capitais ({len(listas_principais['capitais'])} itens):")
    for cidade in listas_principais['capitais']:
        print(f"   - {cidade}")

    print(f"\n3. Destinos para Cidades Interiorana ({len(listas_principais['interior'])} itens):")
    for cidade in listas_principais['interior']:
        print(f"   - {cidade}")

    print(f"\n4. Pacotes de Avião ({len(listas_principais['aviao'])} itens):")
    for cidade in listas_principais['aviao']:
        print(f"   - {cidade}")

    print(f"\n5. Pacotes de Ônibus ({len(listas_principais['onibus'])} itens):")
    for cidade in listas_principais['onibus']:
        print(f"   - {cidade}")

    print(f"\n6. Pacotes de Navio ({len(listas_principais['navio'])} itens):")
    for cidade in listas_principais['navio']:
        print(f"   - {cidade}")

    # Apresenta as novas categorias
    print("\n--- Novas Categorias Geradas ---")
    print(f"• Capitais que são cidades praianas ({len(novas_categorias['capitais_praianas'])}):")
    for cidade in novas_categorias['capitais_praianas']:
        print(f"   - {cidade}")

    print(f"\n• Destinos de praias com pacotes de ônibus ({len(novas_categorias['praias_onibus'])}):")
    for cidade in novas_categorias['praias_onibus']:
        print(f"   - {cidade}")

    print(f"\n• Cidades do interior com pacote de avião ({len(novas_categorias['interior_aviao'])}):")
    if novas_categorias['interior_aviao']:
        for cidade in novas_categorias['interior_aviao']:
            print(f"   - {cidade}")
    else:
        print("   Nenhuma cidade do interior possui pacote de avião.")

    print(f"\n• Cidades com rotas de navio que também são capitais ({len(novas_categorias['capitais_navio'])}):")
    if novas_categorias['capitais_navio']:
        for cidade in novas_categorias['capitais_navio']:
            print(f"   - {cidade}")
    else:
        print("   Nenhuma capital possui rota de navio listada.")

    # Exibe tempos de execução
    tempo_extracao   = fim_extracao - inicio_extracao
    tempo_correlacao = fim_correlacao - inicio_correlacao
    tempo_total      = fim_total - inicio_total

    print("\n--- Tempos de Execução (em segundos) ---")
    print(f"Tempo para extração das listas principais: {tempo_extracao:.4f}s")
    print(f"Tempo para geração das novas categorias: {tempo_correlacao:.4f}s")
    print(f"Tempo total de execução: {tempo_total:.4f}s\n")

if __name__ == '__main__':
    main()
