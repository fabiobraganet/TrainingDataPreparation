import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESIZED_IMAGES_DIR = os.path.join(DATA_DIR, 'output', 'resized_images')
CLASSIFIED_IMAGES_DIR = os.path.join(DATA_DIR, 'output', 'classified_images')
PRE_ANALYSIS_DIR = os.path.join(DATA_DIR, 'pre_analysis')

IMAGES_JSONL_PATH = os.path.join(DATA_DIR, 'images.jsonl')
REPORTS_JSON_PATH = os.path.join(DATA_DIR, 'reports.json')
CLASSES_TRANSLATION_JSON_PATH = os.path.join(DATA_DIR, 'classes_translation.json')
IMAGE_CLASSIFICATIONS_JSON_PATH = os.path.join(DATA_DIR, 'image_classifications.json')

MAX_CONNECTIONS = 5

# Criar pastas se não existirem
os.makedirs(RESIZED_IMAGES_DIR, exist_ok=True)
os.makedirs(CLASSIFIED_IMAGES_DIR, exist_ok=True)
os.makedirs(PRE_ANALYSIS_DIR, exist_ok=True)
os.makedirs(os.path.join(PRE_ANALYSIS_DIR, 'classes'), exist_ok=True)
