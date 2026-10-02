from elasticsearch import Elasticsearch, helpers
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from pathlib import Path
from html import escape



ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "samu"

CIDADES = {
    "LIMOEIRO": 1175,
    "OROBO": 316,
    "CARPINA": 1357,
    "BOM JARDIM": 403,
}

PASTA_SAIDA = Path("pdfs_pesados")
PASTA_SAIDA.mkdir(exist_ok=True)



print("Conectando ao Elasticsearch...")

es = Elasticsearch(ELASTICSEARCH_URL)

if not es.ping():
    print("Elasticsearch não está funcionando.")
    exit()

print("Elasticsearch conectado!")



styles = getSampleStyleSheet()

titulo = ParagraphStyle(
    "Titulo",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    fontSize=16,
    spaceAfter=20
)

campo = ParagraphStyle(
    "Campo",
    parent=styles["Normal"],
    fontSize=10,
    leading=15,
    spaceAfter=5
)



def buscar_ocorrencias(cidade):

    print(f"\nBuscando ocorrências de {cidade}...")

    registros = []

    consulta = {
        "query": {
            "term": {
                "municipio.keyword": cidade
            }
        }
    }

    for hit in helpers.scan(
        es,
        index=INDEX_NAME,
        query=consulta,
        _source=[
            "data",
            "hora_minuto",
            "municipio",
            "bairro",
            "endereco",
            "origem_chamado",
            "tipo",
            "subtipo",
            "sexo",
            "idade",
            "motivo_finalizacao",
            "motivo_desfecho"
        ]
    ):
        registros.append({
            "id": hit["_id"],
            "dados": hit["_source"]
        })

    # Ordem fixa para que os PDFs
    # sem ruído e com ruído tenham
    # exatamente a mesma sequência.
    registros.sort(key=lambda x: x["id"])

    print(f"Encontradas: {len(registros)} ocorrências")

    return registros



def gerar_pdf(cidade, registros):

    nome_arquivo = cidade.replace(" ", "_") + "_sem_ruido.pdf"

    caminho = PASTA_SAIDA / nome_arquivo

    print(f"Gerando: {caminho}")

    documento = SimpleDocTemplate(
        str(caminho),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    elementos = []

    for numero, registro in enumerate(registros, start=1):

        dados = registro["dados"]

        elementos.append(
            Paragraph(
                f"OCORRÊNCIA SAMU - {escape(cidade)}",
                titulo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Página:</b> {numero}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Data:</b> {escape(str(dados.get('data') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Hora:</b> {escape(str(dados.get('hora_minuto') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Município:</b> {escape(str(dados.get('municipio') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Bairro:</b> {escape(str(dados.get('bairro') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Endereço:</b> {escape(str(dados.get('endereco') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Origem do chamado:</b> "
                f"{escape(str(dados.get('origem_chamado') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Tipo:</b> {escape(str(dados.get('tipo') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Subtipo:</b> {escape(str(dados.get('subtipo') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Sexo:</b> {escape(str(dados.get('sexo') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Idade:</b> {escape(str(dados.get('idade') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Motivo da finalização:</b> "
                f"{escape(str(dados.get('motivo_finalizacao') or ''))}",
                campo
            )
        )

        elementos.append(
            Paragraph(
                f"<b>Motivo do desfecho:</b> "
                f"{escape(str(dados.get('motivo_desfecho') or ''))}",
                campo
            )
        )

        # Cada ocorrência começa em uma nova página
        if numero < len(registros):
            elementos.append(PageBreak())

    documento.build(elementos)

    print(f"PDF criado: {caminho}")



for cidade, quantidade_esperada in CIDADES.items():

    registros = buscar_ocorrencias(cidade)

    if len(registros) != quantidade_esperada:
        print(
            f"ATENÇÃO: esperadas {quantidade_esperada}, "
            f"mas encontradas {len(registros)}."
        )

    gerar_pdf(cidade, registros)


print("\n================================")
print("GERAÇÃO CONCLUÍDA")
print("================================")