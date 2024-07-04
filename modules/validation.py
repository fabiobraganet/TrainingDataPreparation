import logging
from PIL import Image, ImageOps
import io

def validate(image_binary, min_occupancy=0.5):
    try:
        image = Image.open(io.BytesIO(image_binary))
        width, height = image.size
        logging.info(f"Validando imagem de tamanho: {width}x{height}")
        if width < 224 or height < 224:
            return False, "Dimensões insuficientes"
        
        # Calcular a taxa de ocupação
        occupied_area = width * height
        target_area = 224 * 224
        occupancy_ratio = occupied_area / target_area

        if occupancy_ratio < min_occupancy:
            return False, f"Taxa de ocupação insuficiente: {occupancy_ratio:.2f}"
        
        return True, "Imagem válida"
    except Exception as e:
        logging.error(f"Erro ao validar a imagem: {e}")
        return False, str(e)
