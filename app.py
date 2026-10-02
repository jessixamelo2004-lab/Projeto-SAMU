from flask import Flask, jsonify, request, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Conexão com o Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Nome do índice
INDEX_NAME = "samu"

@app.route('/')
@app.route('/interface')
def interface():
    return render_template('index.html')

@app.route("/ocorrencias", methods=["GET"])
def ocorrencias():

    filtros = []

    municipio = request.args.get("municipio")
    tipo = request.args.get("tipo")
    sexo = request.args.get("sexo")

    idade_min = request.args.get("idade_min", type=int)
    idade_max = request.args.get("idade_max", type=int)

    data_inicial = request.args.get("data_inicial")
    data_final = request.args.get("data_final")

    # Município
    if municipio:
        filtros.append({
            "match": {
                "municipio": municipio
            }
        })

    # Tipo
    if tipo:
        filtros.append({
            "match": {
                "tipo": tipo
            }
        })

    # Sexo
    if sexo:
        filtros.append({
            "match": {
                "sexo": sexo
            }
        })

    # Idade mínima
    if idade_min is not None:
        filtros.append({
            "range": {
                "idade": {
                    "gte": idade_min
                }
            }
        })

    # Idade máxima
    if idade_max is not None:
        filtros.append({
            "range": {
                "idade": {
                    "lte": idade_max
                }
            }
        })

    # Datas
    if data_inicial or data_final:

        filtro_data = {}

        if data_inicial:
            filtro_data["gte"] = data_inicial

        if data_final:
            filtro_data["lte"] = data_final

        filtros.append({
            "range": {
                "data": filtro_data
            }
        })

    # Montar consulta
    if filtros:
        consulta = {
            "bool": {
                "must": filtros
            }
        }
    else:
        consulta = {
            "match_all": {}
        }

    # Buscar no Elasticsearch
    resultado = es.search(
        index=INDEX_NAME,
        query=consulta,
        size=1000,
        sort=[
            {
                "data": {
                    "order": "desc"
                }
            }
        ]
    )

    registros = []

    for hit in resultado["hits"]["hits"]:

        fonte = hit["_source"]

        registro = {
            "id": hit["_id"],
            "data": fonte.get("data"),
            "hora_minuto": fonte.get("hora_minuto"),
            "municipio": fonte.get("municipio"),
            "bairro": fonte.get("bairro"),
            "endereco": fonte.get("endereco"),
            "origem_chamado": fonte.get("origem_chamado"),
            "tipo": fonte.get("tipo"),
            "subtipo": fonte.get("subtipo"),
            "sexo": fonte.get("sexo"),
            "idade": fonte.get("idade"),
            "motivo_finalizacao": fonte.get("motivo_finalizacao"),
            "motivo_desfecho": fonte.get("motivo_desfecho")
        }

        registros.append(registro)

    return jsonify({
        "total_encontrado": resultado["hits"]["total"]["value"],
        "registros": registros
    })

# ============================================================
# BUSCAR UMA OCORRÊNCIA PELO ID
# ============================================================

@app.route("/ocorrencias/<id>", methods=["GET"])
def buscar_ocorrencia(id):

    try:
        resultado = es.get(
            index=INDEX_NAME,
            id=id
        )

        registro = {
            "id": resultado["_id"],
            **resultado["_source"]
        }

        return jsonify(registro)

    except Exception as e:

        return jsonify({
            "erro": "Ocorrência não encontrada",
            "detalhes": str(e)
        }), 404

@app.route("/ocorrencias", methods=["POST"])
def cadastrar_ocorrencia():

    try:
        dados = request.get_json()

        print("\n========================================")
        print(" NOVA OCORRÊNCIA RECEBIDA")
        print("========================================")
        print("DADOS RECEBIDOS PELO FLASK:")
        print(dados)

        if not dados:
            return jsonify({
                "erro": "Nenhum dado foi enviado"
            }), 400

        # Campos obrigatórios
        campos_obrigatorios = [
            "data",
            "hora_minuto",
            "municipio",
            "bairro",
            "endereco",
            "origem_chamado",
            "tipo",
            "subtipo",
            "sexo",
            "idade"
        ]

        # Verificar os campos
        for campo in campos_obrigatorios:

            if campo not in dados:
                return jsonify({
                    "erro": f"Campo obrigatório não enviado: {campo}"
                }), 400

            if dados[campo] is None or dados[campo] == "":
                return jsonify({
                    "erro": f"Campo obrigatório vazio: {campo}"
                }), 400

        # Garantir tipos corretos
        dados["municipio"] = str(dados["municipio"]).strip().upper()
        dados["bairro"] = str(dados["bairro"]).strip().upper()
        dados["endereco"] = str(dados["endereco"]).strip().upper()
        dados["origem_chamado"] = str(dados["origem_chamado"]).strip().upper()
        dados["tipo"] = str(dados["tipo"]).strip().upper()
        dados["subtipo"] = str(dados["subtipo"]).strip().upper()
        dados["sexo"] = str(dados["sexo"]).strip().upper()
        dados["idade"] = int(dados["idade"])

        print("\nDADOS PROCESSADOS:")
        print("MUNICIPIO:", dados["municipio"])
        print("TIPO:", dados["tipo"])
        print("SEXO:", dados["sexo"])
        print("IDADE:", dados["idade"])
        print("DATA:", dados["data"])
        print("HORA:", dados["hora_minuto"])
        print("BAIRRO:", dados["bairro"])
        print("ENDERECO:", dados["endereco"])
        print("ORIGEM:", dados["origem_chamado"])
        print("SUBTIPO:", dados["subtipo"])

        # Salvar no Elasticsearch
        resultado = es.index(
            index=INDEX_NAME,
            document=dados,
            refresh="wait_for"
        )

        print("\n========================================")
        print(" REGISTRO SALVO NO ELASTICSEARCH")
        print("========================================")
        print("ID:", resultado["_id"])
        print("DADOS SALVOS:", dados)
        print("========================================\n")

        return jsonify({
            "mensagem": "Ocorrência cadastrada com sucesso!",
            "id": resultado["_id"],
            "dados": dados
        }), 201

    except Exception as e:

        print("\n!!!!!!!! ERRO NO CADASTRO !!!!!!!!")
        print(str(e))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

        return jsonify({
            "erro": str(e)
        }), 500
# ============================================================
# EXCLUIR UMA OCORRÊNCIA
# ============================================================

@app.route("/ocorrencias/<id>", methods=["DELETE"])
def excluir_ocorrencia(id):

    try:
        resultado = es.delete(
            index=INDEX_NAME,
            id=id
        )

        return jsonify({
            "mensagem": "Ocorrência excluída com sucesso!",
            "id": id
        })

    except Exception:
        return jsonify({
            "erro": "Ocorrência não encontrada"
        }), 404

    # ============================================================
# ATUALIZAR UMA OCORRÊNCIA
# ============================================================

@app.route("/ocorrencias/<id>", methods=["PUT"])
def atualizar_ocorrencia(id):

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "Nenhum dado foi enviado"
        }), 400

    try:
        resultado = es.update(
            index=INDEX_NAME,
            id=id,
            doc=dados
        )

        return jsonify({
            "mensagem": "Ocorrência atualizada com sucesso!",
            "id": id,
            "dados_atualizados": dados
        })

    except Exception:
        return jsonify({
            "erro": "Ocorrência não encontrada"
        }), 404
# ============================================================
# INICIAR A API
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)