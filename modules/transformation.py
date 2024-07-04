import logging
from PIL import Image, ImageOps
import io

def transform(image_binary, target_size=(224, 224)):
    try:
        image = Image.open(io.BytesIO(image_binary))
        logging.info(f"Transformando imagem para tamanho: {target_size}")
        image.thumbnail(target_size, Image.LANCZOS)
        delta_w = target_size[0] - image.size[0]
        delta_h = target_size[1] - image.size[1]
        padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
        new_image = ImageOps.expand(image, padding)
        return new_image
    except Exception as e:
        logging.error(f"Erro ao transformar a imagem: {e}")
        return None
