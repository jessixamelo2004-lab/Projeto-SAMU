from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

mapeamento = es.indices.get_mapping(index="samu")

print(mapeamento)