from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch("http://localhost:9200")


def ler_idade(mensagem):

    while True:

        idade = input(mensagem)

        if idade == "":
            return None

        try:
            idade = int(idade)

            if idade < 0:
                print("A idade não pode ser negativa.")
                continue

            return idade

        except ValueError:
            print("Digite uma idade válida. Exemplo: 45")


def ler_data(mensagem):

    while True:

        data = input(mensagem)

        if data == "":
            return None

        try:
            datetime.strptime(data, "%Y-%m-%d")
            return data

        except ValueError:
            print("Data inválida. Use o formato AAAA-MM-DD.")


def buscar_ocorrencias():

    print("\n===== BUSCAR OCORRÊNCIAS =====")

    municipio = input("Município (Enter para ignorar): ")
    tipo = input("Tipo (Enter para ignorar): ")
    sexo = input("Sexo (Enter para ignorar): ")

    idade_min = ler_idade(
        "Idade mínima (Enter para ignorar): "
    )

    idade_max = ler_idade(
        "Idade máxima (Enter para ignorar): "
    )

    if idade_min is not None and idade_max is not None:

        if idade_min > idade_max:
            print("A idade mínima não pode ser maior que a idade máxima.")
            return

    data_inicial = ler_data(
        "Data inicial AAAA-MM-DD (Enter para ignorar): "
    )

    data_final = ler_data(
        "Data final AAAA-MM-DD (Enter para ignorar): "
    )

    if data_inicial is not None and data_final is not None:

        if data_inicial > data_final:
            print("A data inicial não pode ser maior que a data final.")
            return

    filtros = []

    if municipio:
        filtros.append({
            "match": {
                "municipio": municipio
            }
        })

    if tipo:
        filtros.append({
            "match": {
                "tipo": tipo
            }
        })

    if sexo:
        filtros.append({
            "match": {
                "sexo": sexo
            }
        })

    if idade_min is not None:
        filtros.append({
            "range": {
                "idade": {
                    "gte": idade_min
                }
            }
        })

    if idade_max is not None:
        filtros.append({
            "range": {
                "idade": {
                    "lte": idade_max
                }
            }
        })

    if data_inicial or data_final:

        filtro_data = {}

        if data_inicial:
            filtro_data["gte"] = data_inicial

        if data_final:
            filtro_data["lte"] = data_final

        filtros.append({
            "range": {
                "data": filtro_data
            }
        })

    if filtros:

        query = {
            "bool": {
                "must": filtros
            }
        }

    else:

        query = {
            "match_all": {}
        }

    try:
        resultado = es.search(
            index="samu",
            query=query
        )

    except Exception as erro:
        print("\nErro ao realizar a busca.")
        print("Verifique se o Elasticsearch está funcionando.")
        return

    print(
        "\nQuantidade encontrada:",
        resultado["hits"]["total"]["value"]
    )

    for registro in resultado["hits"]["hits"]:

        dados = registro["_source"]

        print("\nData:", dados["data"])
        print("Município:", dados["municipio"])
        print("Bairro:", dados["bairro"])
        print("Tipo:", dados["tipo"])
        print("Subtipo:", dados["subtipo"])
        print("Sexo:", dados["sexo"])
        print("Idade:", dados["idade"])
        print("-" * 30)

def buscar_por_periodo():

    print("\n===== BUSCAR POR PERÍODO =====")

    data_inicial = ler_data(
        "Digite a data inicial (AAAA-MM-DD): "
    )

    data_final = ler_data(
        "Digite a data final (AAAA-MM-DD): "
    )

    if data_inicial is not None and data_final is not None:

        if data_inicial > data_final:
            print("A data inicial não pode ser maior que a data final.")
            return

    filtro_data = {}

    if data_inicial:
        filtro_data["gte"] = data_inicial

    if data_final:
        filtro_data["lte"] = data_final

    try:
     resultado = es.search(
        index="samu",
        query={
            "range": {
                "data": filtro_data
            }
        }
    )

    except Exception as erro:
      print("\nErro ao realizar a busca por período.")
      print("Verifique se o Elasticsearch está funcionando.")
      return

    print(
        "\nQuantidade encontrada:",
        resultado["hits"]["total"]["value"]  )


    for registro in resultado["hits"]["hits"]:
        dados = registro["_source"]

        print("\nData:", dados["data"])
        print("Município:", dados["municipio"])
        print("Bairro:", dados["bairro"])
        print("Tipo:", dados["tipo"])
        print("Subtipo:", dados["subtipo"])
        print("Sexo:", dados["sexo"])
        print("Idade:", dados["idade"])
        print("-" * 30)