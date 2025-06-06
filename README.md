prova_np2_codigo.py

Script para leitura e extração de dados estruturados do documento "Prova NP2 - Catálogo de Destinos - PyTravel.docx",
organização em listas e geração de novas categorias por correlação.
Lê o arquivo Word especificado e extrai 6 listas principais conforme seções:
      - Destinos para Cidades Praianas
      - Destinos de Cidades Capitais
      - Destinos de Cidades Interiorana
      - Pacotes de Avião
      - Pacotes de Ônibus
      - Pacotes de Navio

Retorna um dicionário com as listas correspondentes.
Recebe um dicionário com as 6 listas principais e gera novas categorias por correlação:
      - Capitais que são cidades praianas
      - Destinos de praias com pacotes de ônibus
      - Cidades do interior com pacote de avião
      - Cidades com rotas de navio que também são capitais

Retorna um dicionário com essas novas categorias.
Função principal:
      - Registra timestamps de cada etapa
      - Executa a extração das listas
      - Gera as novas categorias por correlação
      - Exibe resultados e tempos de execução
