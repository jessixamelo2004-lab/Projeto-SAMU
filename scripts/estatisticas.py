from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


def estatisticas():

    print("\n===== ESTATÍSTICAS =====")

    try:
        resultado = es.search(
            index="samu",
            size=0,
            aggs={
                "por_tipo": {
                    "terms": {
                        "field": "tipo.keyword"
                    }
                },

                "por_municipio": {
                    "terms": {
                        "field": "municipio.keyword"
                    }
                },

                "por_sexo": {
                    "terms": {
                        "field": "sexo.keyword"
                    }
                },

                "idade_min": {
                    "min": {
                        "field": "idade"
                    }
                },

                "idade_max": {
                    "max": {
                        "field": "idade"
                    }
                },

                "idade_media": {
                    "avg": {
                        "field": "idade"
                    }
                },
                "faixas_etarias": {
                     "range": {
                     "field": "idade",
                     "ranges": [
                     {"to": 18},
                     {"from": 18, "to": 30},
                     {"from": 30, "to": 60},
                     {"from": 60}
        ]
    }
}
            }
        )

    except Exception as erro:
        print("\nErro ao calcular as estatísticas.")
        print("Verifique se o Elasticsearch está funcionando.")
        return

  
    total = resultado["hits"]["total"]["value"]

    print("\nTotal de ocorrências:", total)

    print("\nPor tipo:")

    for item in resultado["aggregations"]["por_tipo"]["buckets"]:
        print(item["key"], ":", item["doc_count"])

    tipos = resultado["aggregations"]["por_tipo"]["buckets"]

    if tipos:
        tipo_mais_frequente = tipos[0]

        print("\nTipo mais frequente:")
        print(tipo_mais_frequente["key"])
        print("Quantidade:", tipo_mais_frequente["doc_count"])

    print("\nPor município:")

    for item in resultado["aggregations"]["por_municipio"]["buckets"]:
        print(item["key"], ":", item["doc_count"])

    municipios = resultado["aggregations"]["por_municipio"]["buckets"]

    if municipios:
        municipio_mais_frequente = municipios[0]

        print("\nMunicípio com mais ocorrências:")
        print(municipio_mais_frequente["key"])
        print("Quantidade:", municipio_mais_frequente["doc_count"])

    print("\nPor sexo:")

    for item in resultado["aggregations"]["por_sexo"]["buckets"]:
        print(item["key"], ":", item["doc_count"])

    idade_min = resultado["aggregations"]["idade_min"]["value"]
    idade_max = resultado["aggregations"]["idade_max"]["value"]
    idade_media = resultado["aggregations"]["idade_media"]["value"]

    print("\nEstatísticas de idade:")
    print("Idade mínima:", idade_min)
    print("Idade máxima:", idade_max)
    print("Idade média:", round(idade_media, 2))
    print("\nFaixas etárias:")

    faixas = resultado["aggregations"]["faixas_etarias"]["buckets"]

    nomes_faixas = [
            "0-17",
           "18-29",
          "30-59",
          "60+"
              ]
    for faixa, nome in zip(faixas, nomes_faixas):
     print(nome, ":", faixa["doc_count"])