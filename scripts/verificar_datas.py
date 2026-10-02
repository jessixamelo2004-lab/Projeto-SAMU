from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

consulta = {
    "query": {
        "range": {
            "data": {
                "gt": "2026-07-31T23:59:59"
            }
        }
    }
}

resultado = es.search(
    index="samu",
    query=consulta["query"],
    size=20
)

print("\n===== REGISTROS POSTERIORES À DATA DA API =====")

for registro in resultado["hits"]["hits"]:

    print("\nID:", registro["_id"])
    print("Dados:", registro["_source"])
    print("-" * 50)

print("\nQuantidade encontrada:", len(resultado["hits"]["hits"]))