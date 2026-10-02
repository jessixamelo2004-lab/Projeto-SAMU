from elasticsearch import Elasticsearch
from datetime import datetime
from consultas import buscar_ocorrencias, buscar_por_periodo
from estatisticas import estatisticas
from cadastrar_ocorrencia import cadastrar_ocorrencia 


es = Elasticsearch("http://localhost:9200")


while True:

    print("\n")
    print("===== SISTEMA SAMU =====")
    print("1 - Buscar ocorrências")
    print("2 - Buscar por período")
    print("3 - Ver estatísticas")
    print("4 - Cadastrar uma nova ocorrência")
    print("5 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        buscar_ocorrencias()

    elif opcao == "2":
        buscar_por_periodo()

    elif opcao == "3":
        estatisticas()

    elif opcao == "4":
        cadastrar_ocorrencia()

    elif opcao == "5":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida!")