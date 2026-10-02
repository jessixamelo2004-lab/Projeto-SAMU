from elasticsearch import Elasticsearch

# Conecta ao Elasticsearch
es = Elasticsearch("http://localhost:9200")

registro = {
    "data": "2026-01-01T00:00:00",
    "hora_minuto": "00:07:13",
    "municipio": "RECIFE",
    "bairro": "TORRE",
    "endereco": "R CONDE DO IRAJA",
    "origem_chamado": "RESIDENCIAL",
    "tipo": "CARDIOLOGICA",
    "subtipo": "PARADA CARDIACA",
    "sexo": "MASCULINO",
    "idade": 77,
    "motivo_finalizacao": None,
    "motivo_desfecho": "1. OCORRÊNCIA CONCLUÍDA COM ÊXITO"
}

# Envia o registro para o Elasticsearch
resposta = es.index(
    index="samu",
    document=registro
)

print("Registro enviado!")
print(resposta)