import requests
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Faz uma requisição POST para /compare")
    parser.add_argument("text", type=str, help="Texto para enviar na consulta")
    parser.add_argument("--top_k", type=int, default=2, help="Número de resultados a retornar")
    args = parser.parse_args()

    url = "http://localhost:8000/compare"
    payload = {
        "text": args.text,
        "top_k": args.top_k
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.ok:
        data = response.json()
        print(json.dumps(data, ensure_ascii=False, indent=4))
    else:
        print(f"Erro na requisição: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()
