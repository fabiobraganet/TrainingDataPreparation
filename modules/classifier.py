import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
import logging
import json
import shutil
import hashlib
import asyncio
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
from utils import config
from modules import report
from concurrent.futures import ThreadPoolExecutor
import global_vars
from tqdm import tqdm  # type: ignore 
from termcolor import colored  

model = MobileNetV2(weights='imagenet')

def classify_image(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)
    decoded_preds = decode_predictions(preds, top=3)[0]
    return decoded_preds

async def classify_images(images, md5_hashes):
    loop = asyncio.get_running_loop()
    logging.info(f"Classifier loop: {loop}")

    results = []
    with ThreadPoolExecutor() as pool:
        for img, md5_hash in tqdm(zip(images, md5_hashes), total=len(images), desc='Classificando imagens', unit='img'):
            tqdm.write(f"{colored(md5_hash, 'blue')}", end='\r')
            result = await loop.run_in_executor(pool, classify_image, img)
            results.append(result)

    return results

def read_classifications_json(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    else:
        return []

def read_classes_translation_json(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    else:
        return []

def write_json(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

async def process_classification(start_time):
    loop = asyncio.get_running_loop()
    logging.info(f"Process classification loop: {loop}")
    classifications = read_classifications_json(config.IMAGE_CLASSIFICATIONS_JSON_PATH)
    classified_images = {entry['md5']: entry['classes'] for entry in classifications}

    classes_translation = read_classes_translation_json(config.CLASSES_TRANSLATION_JSON_PATH)
    existing_classes = {entry['class_id']: entry for entry in classes_translation}

    filenames = [f for f in os.listdir(config.RESIZED_IMAGES_DIR) if f.endswith(".jpg")]
    images = [Image.open(os.path.join(config.RESIZED_IMAGES_DIR, filename)) for filename in filenames]
    md5_hashes = [hashlib.md5(img.tobytes()).hexdigest() for img in images]

    to_classify = []
    for img, md5_hash in zip(images, md5_hashes):
        if md5_hash not in classified_images:
            to_classify.append((img, md5_hash))

    if to_classify:
        imgs_to_classify, hashes_to_classify = zip(*to_classify)
        
        results = await classify_images(imgs_to_classify, hashes_to_classify)

        for img, md5_hash, decoded_preds in zip(imgs_to_classify, hashes_to_classify, results):
            image_classes = []
            for pred in decoded_preds:
                class_id, class_name, score = pred
                class_dir = os.path.join(config.PRE_ANALYSIS_DIR, 'classes', class_name)
                if not os.path.exists(class_dir):
                    os.makedirs(class_dir)
                    global_vars.new_classes_created += 1

                    if class_id not in existing_classes:
                        classes_translation.append({
                            "class_id": class_id,
                            "class_name": class_name,
                            "class_translated": ""
                        })
                        existing_classes[class_id] = {
                            "class_id": class_id,
                            "class_name": class_name,
                            "class_translated": ""
                        }

                shutil.copy(img.filename, class_dir)
                image_classes.append({
                    "class_id": class_id,
                    "class_name": class_name,
                    "score": float(score)
                })
                global_vars.new_class_images += 1

            classifications.append({
                "md5": md5_hash,
                "classes": image_classes
            })
            global_vars.total_processed += 1
            os.remove(img.filename)

    write_json(config.IMAGE_CLASSIFICATIONS_JSON_PATH, classifications)
    write_json(config.CLASSES_TRANSLATION_JSON_PATH, classes_translation)

    report.finalize_report("classify-images", start_time)
