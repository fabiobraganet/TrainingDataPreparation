import os
import json
import logging

def check_and_create_json(file_path):
    """
    Verifica se o arquivo JSON existe e é válido.
    Se não existir, cria um arquivo JSON vazio.
    Se for inválido, avisa e encerra a operação.
    """
    if not os.path.exists(file_path):
        logging.info(f"{file_path} não encontrado. Criando um novo arquivo JSON vazio.")
        with open(file_path, 'w') as f:
            json.dump([], f)
    else:
        try:
            with open(file_path, 'r') as f:
                json.load(f)
        except json.JSONDecodeError:
            logging.error(f"{file_path} é um arquivo JSON inválido. Por favor, corrija o arquivo.")
            raise SystemExit(f"{file_path} é um arquivo JSON inválido. Operação encerrada.")

def validate_json(file_path):
    """
    Verifica se o arquivo JSON é válido.
    Retorna True se for válido, False se for inválido.
    """
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        return False
