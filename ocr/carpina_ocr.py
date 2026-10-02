import easyocr
import pymupdf
import time
import psutil

from elasticsearch import Elasticsearch



PDF = r"pdfs_pesados\CARPINA_sem_ruido.pdf"

ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "ocr"

CIDADE = "CARPINA"
CONDICAO = "sem_ruido"



# CONECTAR AO ELASTICSEARCH


print("Conectando ao Elasticsearch...")

es = Elasticsearch(ELASTICSEARCH_URL)

if not es.ping():
    print("Elasticsearch não está funcionando.")
    exit()

print("Elasticsearch conectado!")


# ABRIR PDF

documento = pymupdf.open(PDF)

total_paginas = len(documento)

print(f"PDF: {PDF}")
print(f"Total de páginas: {total_paginas}")



print("\nCarregando EasyOCR...")

reader = easyocr.Reader(["pt"])

print("EasyOCR carregado!")



# PROCESSAR PÁGINAS


for numero_pagina in range(total_paginas):

    pagina = numero_pagina + 1


    id_documento = f"{CIDADE}_{CONDICAO}_{pagina}"


    
    # VERIFICAR SE JÁ FOI PROCESSADA

    if es.exists(
        index=INDEX_NAME,
        id=id_documento
    ):
        print(
            f"Página {pagina}/{total_paginas} "
            f"já processada. Pulando..."
        )

        continue


    print(
        f"\nProcessando página "
        f"{pagina}/{total_paginas}"
    )


    

    processo = psutil.Process()

    ram_antes = processo.memory_info().rss / (1024 ** 3)



    inicio = time.perf_counter()


    pagina_pdf = documento[numero_pagina]


    # Converter PDF para imagem
    pix = pagina_pdf.get_pixmap(
        matrix=pymupdf.Matrix(2, 2)
    )

    imagem = pix.tobytes("png")


    

    resultado = reader.readtext(
        imagem,
        detail=0
    )


    texto = "\n".join(resultado)



    fim = time.perf_counter()

    tempo = fim - inicio



    ram_depois = processo.memory_info().rss / (1024 ** 3)

    variacao_ram = ram_depois - ram_antes



    # SALVAR NO ELASTICSEARCH

    documento_ocr = {
        "ferramenta": "EasyOCR",
        "arquivo": "CARPINA_sem_ruido.pdf",
        "cidade": CIDADE,
        "condicao": CONDICAO,
        "pagina": pagina,
        "texto": texto,
        "tempo_segundos": tempo,
        "ram_antes_gb": ram_antes,
        "ram_depois_gb": ram_depois,
        "variacao_ram_gb": variacao_ram
    }


    es.index(
        index=INDEX_NAME,
        id=id_documento,
        document=documento_ocr
    )


    print(
        f"Página {pagina} salva no Elasticsearch."
    )

    print(
        f"Tempo: {tempo:.2f} segundos"
    )

    print(
        f"RAM: {ram_antes:.2f} → "
        f"{ram_depois:.2f} GB "
        f"(variação: {variacao_ram:+.2f} GB)"
    )


documento.close()

print("\n===================================")
print("PROCESSAMENTO FINALIZADO")
print("===================================")