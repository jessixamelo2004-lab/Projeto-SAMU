# Projeto SAMU — Monitoramento de Ocorrências e Processamento de OCR

## Sobre o projeto

O projeto SAMU foi desenvolvido inicialmente como uma forma de aprimorar os conhecimentos em **Python, APIs, tratamento de dados, Elasticsearch e Kibana**.

Os dados utilizados são provenientes do **Portal de Dados Abertos da Prefeitura do Recife**, por meio da API de ocorrências do SAMU.

Posteriormente, o projeto passou a incluir o uso de **OCR (Reconhecimento Óptico de Caracteres)** para realizar testes de extração de texto em documentos PDF e, em uma segunda etapa, aplicar o OCR sobre documentos gerados a partir de dados reais do SAMU.

---

## 1. Fonte e dados utilizados

Os dados foram obtidos por meio do Portal de Dados Abertos da Prefeitura do Recife:

[Portal de Dados Abertos — SAMU 2026](https://dados.recife.pe.gov.br/dataset/servico-de-atendimento-movel-de-urgencia-samu-2026?utm_source=chatgpt.com)

### Período dos dados

* Junho de 2026 até setembro de 2026.

Foram selecionadas ocorrências de quatro cidades do interior de Pernambuco:

* Orobó
* Bom Jardim
* Carpina
* Limoeiro

---

## 2. Estrutura do projeto

```text
C:\miniprojetosamu
│   app.py
│   compose.yml
│   main.py
│   README.md
│
├───ocr
│       bomjardim_ocr.py
│       carpina_ocr.py
│       limoeiro_ocr.py
│       orobo_ocr.py
│
├───pdfs_pesados
│       BOM_JARDIM_sem_ruido.pdf
│       CARPINA_sem_ruido.pdf
│       LIMOEIRO_sem_ruido.pdf
│       OROBO_sem_ruido.pdf
│
├───scripts
│       cadastrar_ocorrencia.py
│       comparar_api_elasticsearch.py
│       consultas.py
│       contar_cidade.py
│       contar_por_data.py
│       enviar_elasticsearch.py
│       enviar_varios.py
│       estatisticas.py
│       gerar_pdfs_cidades.py
│       investigar.py
│       remover_registros.py
│       samu.py
│       verificar_datas.py
│       verificar_mapeamento.py
│       verificar_total.py
│
├───static
│       style.css
│
└───templates
        index.html
```

### Principais pastas

**`ocr/`**

Contém os scripts utilizados para executar o OCR sobre os PDFs das cidades:

* `bomjardim_ocr.py`
* `carpina_ocr.py`
* `limoeiro_ocr.py`
* `orobo_ocr.py`

**`pdfs_pesados/`**

Contém os PDFs gerados a partir dos dados das cidades selecionadas.

**`scripts/`**

Contém scripts relacionados à:

* coleta dos dados;
* tratamento;
* consultas;
* estatísticas;
* geração dos PDFs;
* envio para o Elasticsearch;
* verificação dos dados;
* comparação entre API e Elasticsearch;
* cadastro e remoção de ocorrências.

**`static/`**

Contém os arquivos de estilo da aplicação.

**`templates/`**

Contém os arquivos HTML utilizados pela aplicação Flask.

---

# 3. Preparação e tratamento dos dados

O processo inicial do projeto foi realizado a partir dos dados disponibilizados pela API do SAMU.

Fluxo geral:

```text
API Dados Recife
       ↓
Coleta dos dados
       ↓
Tratamento dos dados
       ↓
Seleção das cidades
       ↓
Armazenamento no Elasticsearch
       ↓
Consultas e análises
       ↓
Visualização no Kibana
```

Foram selecionadas as ocorrências referentes às cidades:

* Orobó
* Bom Jardim
* Carpina
* Limoeiro

---

# 4. Docker + Elasticsearch + Kibana

O projeto utiliza **Docker Compose** para executar o Elasticsearch e o Kibana.

### Elasticsearch

Versão utilizada:

```text
Elasticsearch 9.4.4
```

Acesso:

```text
http://localhost:9200
```

### Kibana

Versão utilizada:

```text
Kibana 9.4.4
```

Acesso:

```text
http://localhost:5601
```

### Índices utilizados

Foram utilizados principalmente dois índices:

```text
samu
ocr
```

O índice `samu` armazena os dados das ocorrências.

O índice `ocr` é utilizado para armazenar informações relacionadas ao processamento e à extração de texto dos documentos.

---

# 5. Kibana

O Kibana foi utilizado para realizar a exploração e visualização dos dados armazenados no Elasticsearch.

Foram utilizadas consultas e visualizações para analisar informações como:

* quantidade de ocorrências;
* idade;
* sexo;
* bairro;
* cidade;
* período das ocorrências.

Essas informações podem ser apresentadas por meio de gráficos e dashboards.

---

# 6. Flask + Front-end

Foi desenvolvida uma aplicação utilizando **Flask** para permitir a interação com os dados armazenados no Elasticsearch.

Fluxo da aplicação:

```text
Front-end
    ↓
Flask
    ↓
Elasticsearch
    ↓
Dados do SAMU
```

A aplicação possui operações CRUD:

| Método | Rota          | Função               |
| ------ | ------------- | -------------------- |
| GET    | `/dados`      | Consultar dados      |
| POST   | `/dados`      | Cadastrar ocorrência |
| PUT    | `/dados/<id>` | Atualizar ocorrência |
| DELETE | `/dados/<id>` | Remover ocorrência   |

---

# 7. OCR

O OCR foi incorporado ao projeto em **duas etapas diferentes**.

É importante destacar que os primeiros testes de OCR **não foram realizados utilizando os dados da API do SAMU**.

---

## 7.1 Primeira etapa — Comparação entre ferramentas de OCR

Inicialmente foram criados **dois PDFs específicos para testar OCR**:

* um PDF sem ruídos;
* um PDF com ruídos.

Esses documentos foram utilizados exclusivamente para comparar diferentes ferramentas de OCR.

As ferramentas testadas foram:

* **Baidu OCR**
* **DocTR**
* **EasyOCR**
* **PaddleOCR**

Cada ferramenta possui um script em Python responsável por realizar a leitura do documento e comparar o texto esperado com o texto extraído.

### Métricas analisadas

Foram considerados:

* qualidade da extração;
* **CER (Character Error Rate)**;
* **WER (Word Error Rate)**;
* tempo de processamento;
* utilização de memória RAM.

### CER

O **CER (Character Error Rate)** mede a quantidade de erros encontrados nos caracteres extraídos pelo OCR.

Quanto menor o CER, menor é a quantidade de erros de caracteres.

### WER

O **WER (Word Error Rate)** mede os erros encontrados nas palavras extraídas.

Quanto menor o WER, menor é a quantidade de erros nas palavras.

### Fluxo dos testes iniciais

```text
PDF sem ruído ─────┐
                   ├──→ Baidu OCR
PDF com ruído ─────┤
                   ├──→ DocTR
                   ├──→ EasyOCR
                   └──→ PaddleOCR
                            ↓
                     Texto extraído
                            ↓
                  Comparação com texto
                       esperado
                            ↓
                    CER / WER / Tempo
                       / Memória RAM
```

---

# 8. Segunda etapa — OCR aplicado aos dados do SAMU

Após os testes iniciais, o OCR foi aplicado aos **dados reais do SAMU**.

Nesta etapa, os dados foram obtidos pela API e foram selecionadas ocorrências das seguintes cidades:

* Orobó
* Bom Jardim
* Carpina
* Limoeiro

Os dados selecionados foram transformados em documentos PDF.

Nesta etapa, foi utilizado **EasyOCR** para realizar a extração do texto.

---

# 9. Geração dos PDFs

Foi criado o script:

```text
scripts/gerar_pdfs_cidades.py
```

Esse script utiliza os dados selecionados para gerar os documentos PDF.

Cada ocorrência é representada em uma página do PDF.

Exemplo:

```text
PDF OROBÓ

Página 1 → Ocorrência 1
Página 2 → Ocorrência 2
Página 3 → Ocorrência 3
...
```

O mesmo processo é realizado para as demais cidades.

Os PDFs gerados estão na pasta:

```text
pdfs_pesados/
```

---

# 10. EasyOCR aplicado aos PDFs do SAMU

Depois da geração dos PDFs, os documentos foram processados utilizando **EasyOCR**.

Foram criados scripts específicos para cada cidade:

```text
ocr/
├── bomjardim_ocr.py
├── carpina_ocr.py
├── limoeiro_ocr.py
└── orobo_ocr.py
```

O processamento segue o fluxo:

```text
Dados do SAMU
      ↓
Seleção das cidades
      ↓
Geração dos PDFs
      ↓
PDF com uma ocorrência por página
      ↓
EasyOCR
      ↓
Texto extraído
      ↓
Armazenamento / análise
```

---

# 11. Fluxo geral do projeto

O projeto possui dois fluxos relacionados ao OCR.

### Fluxo 1 — Testes e comparação das ferramentas

```text
PDFs de teste
     ↓
PDF sem ruído + PDF com ruído
     ↓
Baidu / DocTR / EasyOCR / PaddleOCR
     ↓
Extração do texto
     ↓
Comparação com texto esperado
     ↓
CER / WER / tempo / RAM
```

### Fluxo 2 — Aplicação sobre dados reais do SAMU

```text
API Dados Recife
       ↓
Dados reais do SAMU
       ↓
Seleção das cidades
       ↓
Orobó / Bom Jardim / Carpina / Limoeiro
       ↓
Geração dos PDFs
       ↓
Uma ocorrência por página
       ↓
EasyOCR
       ↓
Extração do texto
       ↓
Armazenamento e análise
```

---

# 12. Objetivos do projeto

O projeto tem como principais objetivos:

* estudar Python na prática;
* trabalhar com APIs;
* realizar tratamento e organização de dados;
* utilizar Elasticsearch para armazenamento e consultas;
* utilizar Kibana para visualização dos dados;
* desenvolver uma aplicação com Flask;
* compreender o funcionamento de ferramentas de OCR;
* comparar diferentes ferramentas de OCR em documentos de teste;
* avaliar a qualidade da extração utilizando CER e WER;
* analisar tempo de processamento e utilização de memória;
* aplicar OCR sobre documentos gerados a partir de dados reais do SAMU.

---

# 13. Tecnologias utilizadas

* Python
* Flask
* Docker
* Docker Compose
* Elasticsearch 9.4.4
* Kibana 9.4.4
* EasyOCR
* Baidu OCR
* DocTR
* PaddleOCR
* API Dados Recife
* HTML
* CSS
* PowerShell
