from ckanapi import RemoteCKAN
from elasticsearch import Elasticsearch, helpers
import hashlib
import json


RESOURCE_ID = "d6f586c3-34c5-4414-9804-6fdfbd75c7db"

API_URL = "https://dados.recife.pe.gov.br/pt_BR/"
ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "samu"

TAMANHO_LOTE = 500


def limpar_registro(registro):

    registro.pop("_id", None)

    for campo in registro:
        if isinstance(registro[campo], str):
            registro[campo] = registro[campo].strip()

    for campo in registro:
        if registro[campo] == "":
            registro[campo] = None

    idade = registro.get("idade")

    if idade is None:
        registro["idade"] = None
    else:
        try:
            registro["idade"] = int(idade)
        except (ValueError, TypeError):
            registro["idade"] = None

    return registro


def gerar_id(registro):

    texto = json.dumps(
        registro,
        sort_keys=True,
        ensure_ascii=False
    )

    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()


print("Conectando ao Elasticsearch...")

es = Elasticsearch(ELASTICSEARCH_URL)

if not es.ping():
    print("Elasticsearch não está funcionando.")
    exit()

print("Elasticsearch conectado!")


print("Conectando à API...")

rc = RemoteCKAN(API_URL)

print("API conectada!")


# ============================================================
# PEGAR TOTAL DA API
# ============================================================

resultado = rc.action.datastore_search(
    resource_id=RESOURCE_ID,
    limit=1
)

total = resultado["total"]

print(f"\nTotal na API: {total}")


# ============================================================
# GERAR TODOS OS IDs DA API
# ============================================================

ids_api = set()

print("\nGerando IDs dos registros da API...")

for inicio in range(0, total, TAMANHO_LOTE):

    resultado = rc.action.datastore_search(
        resource_id=RESOURCE_ID,
        limit=TAMANHO_LOTE,
        offset=inicio
    )

    registros = resultado["records"]

    for registro in registros:

        registro = limpar_registro(registro)

        id_registro = gerar_id(registro)

        ids_api.add(id_registro)

    print(
        f"Processados na API: "
        f"{min(inicio + len(registros), total)} / {total}"
    )


print("\nIDs gerados pela API:", len(ids_api))


# ============================================================
# PEGAR TODOS OS IDs DO ELASTICSEARCH
# ============================================================

print("\nBuscando IDs do Elasticsearch...")

ids_elasticsearch = set()

for documento in helpers.scan(
    es,
    index=INDEX_NAME,
    query={
        "query": {
            "match_all": {}
        },
        "_source": False
    }
):

    ids_elasticsearch.add(documento["_id"])


print(
    "IDs no Elasticsearch:",
    len(ids_elasticsearch)
)


# ============================================================
# DESCOBRIR DOCUMENTOS EXTRAS
# ============================================================

extras = ids_elasticsearch - ids_api

print("\n========================================")
print("RESULTADO DA COMPARAÇÃO")
print("========================================")

print("Total na API:", len(ids_api))

print(
    "Total no Elasticsearch:",
    len(ids_elasticsearch)
)

print(
    "Documentos extras:",
    len(extras)
)


# ============================================================
# MOSTRAR OS EXTRAS
# ============================================================

if extras:

    print("\n===== IDS EXTRAS =====")

    for id_extra in extras:

        print(id_extra)

else:

    print("\nNenhum documento extra encontrado.")