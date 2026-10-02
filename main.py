from ckanapi import RemoteCKAN
from elasticsearch import Elasticsearch, helpers
import hashlib
import json


# ============================================================
# CONFIGURAÇÕES
# ============================================================

RESOURCE_ID = "d6f586c3-34c5-4414-9804-6fdfbd75c7db"

API_URL = "https://dados.recife.pe.gov.br/pt_BR/"

ELASTICSEARCH_URL = "http://localhost:9200"

INDEX_NAME = "samu"

# A API do Recife está retornando no máximo 500 registros
# por requisição.
TAMANHO_LOTE = 500


# ============================================================
# CONEXÃO COM ELASTICSEARCH
# ============================================================

print("Conectando ao Elasticsearch...")

es = Elasticsearch(ELASTICSEARCH_URL)

if not es.ping():
    print("Erro: Elasticsearch não está funcionando.")
    exit()

print("Elasticsearch conectado com sucesso!")


# ============================================================
# CONEXÃO COM A API DO RECIFE
# ============================================================

print("Conectando à API do Portal Recife...")

rc = RemoteCKAN(API_URL)

print("API conectada com sucesso!")


# ============================================================
# FUNÇÃO PARA LIMPAR OS REGISTROS
# ============================================================

def limpar_registro(registro):

    # Remove o ID interno criado pelo CKAN
    registro.pop("_id", None)

    # Remove espaços desnecessários
    for campo in registro:

        if isinstance(registro[campo], str):
            registro[campo] = registro[campo].strip()

    # Transforma campos vazios em None
    for campo in registro:

        if registro[campo] == "":
            registro[campo] = None

    # Trata a idade
    idade = registro.get("idade")

    if idade is None:
        registro["idade"] = None

    else:
        try:
            registro["idade"] = int(idade)

        except (ValueError, TypeError):
            registro["idade"] = None

    return registro


# ============================================================
# GERA UM ID ÚNICO PARA CADA REGISTRO
# ============================================================

def gerar_id(registro):

    texto = json.dumps(
        registro,
        sort_keys=True,
        ensure_ascii=False
    )

    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()


# ============================================================
# DESCOBRE QUANTOS REGISTROS EXISTEM NA API
# ============================================================

print("\nConsultando quantidade de registros...")

resultado = rc.action.datastore_search(
    resource_id=RESOURCE_ID,
    limit=1
)

total = resultado["total"]

print(f"Total de registros na API: {total:,}")


# ============================================================
# IMPORTAÇÃO
# ============================================================

print("\n===== INICIANDO IMPORTAÇÃO =====")

total_processados = 0
total_erros = 0
lote_numero = 0


for inicio in range(0, total, TAMANHO_LOTE):

    lote_numero += 1

    fim = min(inicio + TAMANHO_LOTE, total)

    print(
        f"\nLote {lote_numero} "
        f"→ registros {inicio + 1} até {fim}"
    )

    # --------------------------------------------------------
    # BUSCA O LOTE NA API
    # --------------------------------------------------------

    try:

        resultado = rc.action.datastore_search(
            resource_id=RESOURCE_ID,
            limit=TAMANHO_LOTE,
            offset=inicio
        )

        registros = resultado["records"]

    except Exception as erro:

        print("\nErro ao buscar dados da API:")
        print(erro)

        continue


    # --------------------------------------------------------
    # VERIFICA SE A API RETORNOU DADOS
    # --------------------------------------------------------

    if not registros:

        print("Nenhum registro retornado neste lote.")
        continue


    print(
        f"Registros recebidos da API: {len(registros)}"
    )


    # --------------------------------------------------------
    # PREPARA OS DOCUMENTOS
    # --------------------------------------------------------

    documentos = []

    for registro in registros:

        registro = limpar_registro(registro)

        documento = {
            "_index": INDEX_NAME,
            "_id": gerar_id(registro),
            "_source": registro
        }

        documentos.append(documento)


    # --------------------------------------------------------
    # ENVIA PARA O ELASTICSEARCH
    # --------------------------------------------------------

    try:

        sucesso, erros = helpers.bulk(
            es,
            documentos,
            chunk_size=TAMANHO_LOTE,
            raise_on_error=False
        )

        total_processados += sucesso

        total_erros += len(erros)

        print(
            f"Sucesso neste lote: {sucesso}"
        )

        if erros:

            print(
                f"Erros neste lote: {len(erros)}"
            )

    except Exception as erro:

        print(
            "\nErro ao enviar lote para o Elasticsearch:"
        )

        print(erro)

        total_erros += len(documentos)


# ============================================================
# FINALIZAÇÃO
# ============================================================

print("\n========================================")
print("IMPORTAÇÃO FINALIZADA")
print("========================================")

print(
    f"Total encontrado na API: {total}"
)

print(
    f"Total processado com sucesso: "
    f"{total_processados}"
)

print(
    f"Total de erros: {total_erros}"
)


# ============================================================
# CONFERE QUANTOS DOCUMENTOS EXISTEM NO ELASTICSEARCH
# ============================================================

print(
    "\nVerificando quantidade no Elasticsearch..."
)

try:

    resultado = es.count(
        index=INDEX_NAME
    )

    total_elasticsearch = resultado["count"]

    print(
        f"Total de documentos no índice "
        f"'{INDEX_NAME}': {total_elasticsearch}"
    )

except Exception as erro:

    print(
        "Não foi possível consultar o total."
    )

    print(erro)


# ============================================================
# FIM
# ============================================================

print("\nProcesso concluído!")