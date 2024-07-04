import os
import json
import logging
import asyncio
from modules.collector import Collector
from modules import validation, transformation, report
from utils import config
import global_vars
from tqdm import tqdm  # type: ignore # Biblioteca para barra de progresso
from termcolor import colored  # Biblioteca para colorir texto no terminal

async def run(start_time):
    collector = Collector(max_connections=50)

    if not os.path.exists(config.IMAGES_JSONL_PATH):
        logging.info("Sem dados para coletar")
        return

    urls = []
    with open(config.IMAGES_JSONL_PATH, 'r') as f:
        for line in f:
            global_vars.total_read += 1
            data = json.loads(line)
            url = data.get("url")
            if url:
                urls.append(url)
    
    logging.info(f"Total de URLs a serem processados: {len(urls)}")

    images = await collector.collect_images(urls)
    
    # Usando tqdm para mostrar a barra de progresso
    for image_binary, url in tqdm(zip(images, urls), total=len(urls), desc='Coletando imagens', unit='url'):
        tqdm.write(f"{colored(url, 'blue')}")
        if image_binary and isinstance(image_binary, bytes):
            logging.info(f"Processando imagem da URL: {url}, tamanho: {len(image_binary)} bytes")
            try:
                is_valid, reason = validation.validate(image_binary)
                if is_valid:
                    transformed_image = transformation.transform(image_binary)
                    if transformed_image:
                        report.log_image(transformed_image)
                else:
                    logging.info(f"Imagem recusada: {reason}")
                    if "Dimensões insuficientes" in reason:
                        global_vars.total_rejected_by_dimension += 1
                    else:
                        global_vars.total_rejected_by_occupancy += 1
            except Exception as e:
                logging.error(f"Erro ao validar a imagem da URL {url}: {e}")
                global_vars.total_errors += 1
        else:
            if isinstance(image_binary, bytes):
                logging.error(f"Erro ao validar a imagem da URL {url}: Imagem binária vazia ou erro na coleta")
            else:
                logging.error(f"Erro ao validar a imagem da URL {url}: {image_binary}")
            global_vars.total_url_errors += 1
    await collector.close()
