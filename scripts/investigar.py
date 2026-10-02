from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

ids_extras = [
    "Ak3uOaABuFxWIGyNJjQA",
    "A03uOaABuFxWIGyNJjQ_",
    "hU3dOaABuFxWIGyN6jNV",
    "BE3uOaABuFxWIGyNJjRz"
]

print("\n===== DOCUMENTOS EXTRAS =====")

for id_documento in ids_extras:

    try:
        resultado = es.get(
            index="samu",
            id=id_documento
        )

        print("\nID:", id_documento)
        print("Dados:", resultado["_source"])

    except Exception as erro:
        print(f"\nErro ao buscar {id_documento}:")
        print(erro)