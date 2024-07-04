import os
import logging
from modules import classifier
from utils import config

async def run(start_time):
    if not os.path.exists(config.RESIZED_IMAGES_DIR):
        logging.info("Sem imagens redimensionadas para classificar")
        return

    await classifier.process_classification(start_time)

