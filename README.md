# Plagio Detector

Detector de plágio utilizando análises lexicais e semânticas em textos.

## Funcionalidades

Este projeto oferece uma API para comparar um texto de entrada com um corpus de documentos, identificando possíveis plágios através de duas metodologias principais:

**- Análise Lexical:** Compara a frequência e a similaridade de palavras entre os textos (TF-IDF + similaridade por cosseno)

**- Análise Semântica:** Utiliza modelos de embeddings (por default, `sentence-transformers/all-MiniLM-L6-v2`) para entender o significado e a similaridade contextual entre os textos.

## Como rodar localmente

1. Criar ambiente virtual e instalar dependências

    ```bash
    virtualenv venv --python=3.10
    . venv/bin/activate
    pip install -r requirements.txt
    ```

2. Inicializar corpus de documentos

    Antes de rodar o servidor, é necessário baixar e preparar os documentos que serão usados para comparação. Para isso, execute o script abaixo, na pasta `app`:

    ```bash python setup_data.py [--query "{sua_consulta}"]```

    Esse script:

    - Baixa artigos mais relevantes da Wikipedia em português de acordo com a query (default: "inteligência artificial").

    - Salva cada documento em `app/data/docs` usando como nome o hash SHA-256 do conteúdo (garantindo unicidade).

    - Gera o arquivo `app/data/metadata.csv` que mapeia cada hash para o título original do artigo na Wikipedia.

3. Rodar o servidor FastAPI

    Depois de ativar o ambiente virtual, instalar as dependências e inicializar os dados, inicie o servidor:

    ```bash uvicorn app.main:app --reload```

    O servidor estará disponível em: `http://localhost:8000`.

## Como rodar com Docker

Se você preferir usar o Docker, pode construir a imagem e rodar o container facilmente.

1. Build da imagem

    Na pasta raiz do projeto, execute o comando para construir a imagem:

    ```bash docker build -t plagio-detector .```

    Durante a construção ou na primeira execução do container, a aplicação verifica se o diretório `app/data/docs` contém documentos.

    Se estiver vazio ou não existir, o script de inicialização será executado automaticamente para baixar e preparar os documentos do corpus a partir da query padrão "inteligência artificial".

    Caso já existam documentos na pasta, a inicialização será pulada.

2. Rodar o container

    Agora, inicie o container, mapeando a porta local 8000 para a porta do container:

    ```bash docker run -p 8000:8000 plagio-detector```

    O servidor também estará disponível em: `http://localhost:8000`.


## Endpoints da API

### Health Check

Verifica se a aplicação está funcionando corretamente.

- Método: GET

- URL: /health

```bash
curl -X GET "http://localhost:8000/health"
```

Exemplo de resposta:

```json
{
    "status": "ok"
}
```

## Comparar textos

Recebe um texto para verificar plágio e o compara com o corpus de documentos.

- Método: POST

- URL: /compare

- Corpo da requisição (JSON):
    - **text:** O texto a ser verificado.
    - **top_k (opcional):** O número de resultados mais relevantes para retornar (o padrão é 5).


```bash
curl -X POST "http://localhost:8000/compare" \
     -H "Content-Type: application/json" \
     -d '{"text": "{texto a ser comparado}", "top_k": K}'
```

ou a partir do script python fornecido:

```bash
python3 get_result.py "{texto a ser comparado}" [--top_k K]
```
- K (opcional): número de resultados relevantes que deseja que seja exibido


Exemplo de requisição:

```bash
curl -X POST "http://localhost:8000/compare" \
     -H "Content-Type: application/json" \
     -d '{"text": "OpenAI é uma empresa de IA", "top_k": 2}'
```
Exemplo de resposta:

```json
{
"lexical": [
    {
    "doc_id": "e97fef016f9d55c575daafacafd17e7353397d4871cfc7234169e8fa482b3417",
    "title": "OpenAI",
    "similarity": 0.24209551760814907,
    "texto": "OpenAI é uma empresa e laboratório de pesquisa de inteligência artificial (IA) estadunidense que consiste na organização sem fins lucrativos OpenAI Incorporated (OpenAI Inc.) e sua subsidiária com fin"
    },
    ...
],
"semantic": [
    {
    "doc_id": "9199acbf6343bf5aa23a839d3b0af9551e0921213dee4e9de528a6ff2dcb59e1",
    "title": "Mira Murati",
    "similarity": 0.6908043622970581,
    "texto": "Mira Murati é uma engenheira albanesa ex-diretora executiva  da OpenAI, que mora nos Estados Unidos. Ela é diretora de tecnologia da OpenAI, empresa que desenvolve o ChatGPT, um chatbot de inteligênci"
    },
    ...
]
}
```


