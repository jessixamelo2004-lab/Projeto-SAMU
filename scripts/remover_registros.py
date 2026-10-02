from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

# IDs dos registros extras que queremos remover
ids_para_remover = [
    "Ak3uOaABuFxWIGyNJjQA",
    "A03uOaABuFxWIGyNJjQ_",
    "hU3dOaABuFxWIGyN6jNV",
    "BE3uOaABuFxWIGyNJjRz",
    "5R2VWKABRTOsc8KUQvRc"
]

print("\n===== REMOVENDO REGISTROS EXTRAS =====")

for id_documento in ids_para_remover:

    try:
        resultado = es.delete(
            index="samu",
            id=id_documento
        )

        print(
            f"Registro {id_documento} removido: "
            f"{resultado['result']}"
        )

    except Exception as erro:
        print(f"Erro ao remover {id_documento}:")
        print(erro)

print("\nProcesso finalizado.")