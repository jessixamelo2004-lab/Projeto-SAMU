from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch("http://localhost:9200")


def cadastrar_ocorrencia():

    print("\n===== CADASTRAR OCORRÊNCIA =====")

    # Data
    while True:
        data = input("Data (AAAA-MM-DD): ")

        try:
            datetime.strptime(data, "%Y-%m-%d")
            break
        except ValueError:
            print("Data inválida. Use o formato AAAA-MM-DD.")

    # Hora
    while True:
        hora = input("Hora (HH:MM:SS): ")

        try:
            datetime.strptime(hora, "%H:%M:%S")
            break
        except ValueError:
            print("Hora inválida. Use o formato HH:MM:SS.")

    # Dados da ocorrência
    municipio = input("Município: ").upper()
    bairro = input("Bairro: ").upper()
    endereco = input("Endereço: ").upper()
    origem = input("Origem do chamado: ").upper()
    tipo = input("Tipo: ").upper()
    subtipo = input("Subtipo: ").upper()
    sexo = input("Sexo: ").upper()

    # Idade
    while True:
        try:
            idade = int(input("Idade: "))

            if idade < 0:
                print("A idade não pode ser negativa.")
                continue

            break

        except ValueError:
            print("Digite uma idade válida.")

    # Documento que será enviado para o Elasticsearch
    documento = {
        "data": data + "T" + hora,
        "hora_minuto": hora,
        "municipio": municipio,
        "bairro": bairro,
        "endereco": endereco,
        "origem_chamado": origem,
        "tipo": tipo,
        "subtipo": subtipo,
        "sexo": sexo,
        "idade": idade
    }

    # Cadastro no Elasticsearch
    try:
        resultado = es.index(
            index="samu",
            document=documento
        )

        print("\nOcorrência cadastrada com sucesso!")
        print("ID:", resultado["_id"])

    except Exception as erro:
        print("\nErro ao cadastrar ocorrência.")
        print("Detalhes do erro:", erro)