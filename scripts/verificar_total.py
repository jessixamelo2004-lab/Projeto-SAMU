from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

resultado = es.count(index="samu")

print("Total de registros no Elasticsearch:", resultado["count"])