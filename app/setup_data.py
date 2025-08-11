import requests
import os
import hashlib
import csv
import argparse

CORPUS_DIR = "data/docs"
os.makedirs(CORPUS_DIR, exist_ok=True)

DATA_DIR = os.path.dirname(CORPUS_DIR) 

API_URL = "https://pt.wikipedia.org/w/api.php"
NUM_DOCUMENTS = 200

def get_query_article_titles(api_url, query, num_articles):
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'srlimit': num_articles,
        'format': 'json'
    }
    try:
        response = requests.get(api_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return [result['title'] for result in data['query']['search']]
    except requests.RequestException as e:
        print(f"Erro ao buscar artigos relacionados a '{query}': {e}")
        return []

def get_article_content(api_url, title):
    params = {
        'action': 'query',
        'prop': 'extracts',
        'explaintext': True,
        'titles': title,
        'format': 'json',
        'exlimit': 1,
        'exintro': False,
        'redirects': True
    }
    try:
        response = requests.get(api_url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        pages = data['query']['pages']
        page_id = next(iter(pages))
        content = pages[page_id].get('extract', '')
        return os.linesep.join([s for s in content.splitlines() if s])
    except requests.RequestException as e:
        print(f"Erro ao baixar o conteúdo do artigo '{title}': {e}")
        return None

def initialize_data(search_query):
    print(f"Iniciando a construção do corpus de documentos da Wikipedia sobre '{search_query}'...")

    article_titles = get_query_article_titles(API_URL, search_query, NUM_DOCUMENTS)

    if not article_titles:
        print("Não foi possível obter os títulos dos artigos.")
        return

    downloaded_count = 0
    mapping_file = os.path.join(DATA_DIR, "metadata.csv")

    with open(mapping_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "title"])

        for title in article_titles:
            if downloaded_count >= NUM_DOCUMENTS:
                break

            cleaned_text = get_article_content(API_URL, title)

            if cleaned_text:
                hash_id = hashlib.sha256(cleaned_text.encode('utf-8')).hexdigest()
                file_path = os.path.join(CORPUS_DIR, f"{hash_id}.txt")

                if not os.path.exists(file_path):
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(cleaned_text)

                        writer.writerow([hash_id, title])
                        downloaded_count += 1
                        print(f"Documento {downloaded_count}/{NUM_DOCUMENTS} salvo como ID: {hash_id[:8]}...")
                    except OSError as e:
                        print(f"Erro ao salvar o arquivo '{file_path}': {e}")
                else:
                    print(f"Documento com ID {hash_id[:8]} já existe, pulando...")
                    downloaded_count += 1

    print(f"\nCorpus de {downloaded_count} documentos criado com sucesso na pasta '{CORPUS_DIR}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inicializa o corpus de documentos da Wikipedia.")
    parser.add_argument("--query", type=str, default="inteligência artificial", help="Termo de busca para artigos da Wikipedia.")
    args = parser.parse_args()

    if not os.path.exists(CORPUS_DIR) or not os.listdir(CORPUS_DIR):
        print(f"Corpus directory '{CORPUS_DIR}' is empty or missing. Initializing data...")
        initialize_data(args.query)
    else:
        print(f"Corpus directory '{CORPUS_DIR}' already has data. Skipping initialization.")

    print("Setup complete.")
