from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "samu"

CIDADE = "OROBO"

print("Conectando ao Elasticsearch...")

es = Elasticsearch(ELASTICSEARCH_URL)

if not es.ping():
    print("Elasticsearch não está funcionando.")
    exit()

print("Elasticsearch conectado!")

resultado = es.count(
    index=INDEX_NAME,
    query={
        "term": {
            "municipio.keyword": CIDADE
        }
    }
)

print(f"\nCidade: {CIDADE}")
print(f"Quantidade de ocorrências: {resultado['count']}")