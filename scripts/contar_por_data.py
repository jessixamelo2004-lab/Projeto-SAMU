from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

resultado = es.search(
    index="samu",
    size=0,
    aggs={
        "por_data": {
            "terms": {
                "field": "data",
                "size": 500
            }
        }
    }
)

print("\n===== QUANTIDADE POR DATA =====")

for item in resultado["aggregations"]["por_data"]["buckets"]:
    print(item["key"], ":", item["doc_count"])