from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

registros = [
    {
        "data": "2026-01-02T10:30:00",
        "hora_minuto": "10:30:00",
        "municipio": "RECIFE",
        "bairro": "BOA VIAGEM",
        "endereco": "AV BOA VIAGEM",
        "origem_chamado": "RESIDENCIAL",
        "tipo": "TRAUMA",
        "subtipo": "QUEDA",
        "sexo": "FEMININO",
        "idade": 45,
        "motivo_finalizacao": None,
        "motivo_desfecho": "1. OCORRÊNCIA CONCLUÍDA COM ÊXITO"
    },
    {
        "data": "2026-01-03T14:20:00",
        "hora_minuto": "14:20:00",
        "municipio": "RECIFE",
        "bairro": "CASA AMARELA",
        "endereco": "ESTRADA DO ARRAIAL",
        "origem_chamado": "RESIDENCIAL",
        "tipo": "CLINICA",
        "subtipo": "MAL ESTAR",
        "sexo": "MASCULINO",
        "idade": 62,
        "motivo_finalizacao": None,
        "motivo_desfecho": "1. OCORRÊNCIA CONCLUÍDA COM ÊXITO"
    },
    {
        "data": "2026-01-04T18:45:00",
        "hora_minuto": "18:45:00",
        "municipio": "OLINDA",
        "bairro": "CENTRO",
        "endereco": "AV SIGISMUNDO GONCALVES",
        "origem_chamado": "VIA PUBLICA",
        "tipo": "TRAUMA",
        "subtipo": "ACIDENTE",
        "sexo": "MASCULINO",
        "idade": 29,
        "motivo_finalizacao": None,
        "motivo_desfecho": "1. OCORRÊNCIA CONCLUÍDA COM ÊXITO"
    }
]

for registro in registros:
    resposta = es.index(index="samu", document=registro)
    print("Registro enviado:", resposta["_id"])