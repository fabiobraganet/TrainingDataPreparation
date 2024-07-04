import hashlib
import logging
import os
import json
from datetime import datetime
from utils import config
import global_vars

def log_image(image):
    try:
        md5_hash = hashlib.md5(image.tobytes()).hexdigest()
        image_path = os.path.join(config.RESIZED_IMAGES_DIR, f"{md5_hash}.jpg")
        image.save(image_path)
        logging.info(f"Imagem salva em: {image_path}")
        global_vars.total_saved += 1
    except Exception as e:
        logging.error(f"Erro ao salvar a imagem: {e}")

def finalize_report(report_type, start_time):
    if report_type == "resize-images":
        report_entry = {
            "timestamp": start_time,
            "report_type": report_type,
            "total_read": global_vars.total_read,
            "total_rejected_by_dimension": global_vars.total_rejected_by_dimension,
            "total_rejected_by_occupancy": global_vars.total_rejected_by_occupancy,
            "total_already_existed": global_vars.total_already_existed,
            "total_saved": global_vars.total_saved,
            "total_url_errors": global_vars.total_url_errors,
            "total_processed": global_vars.total_processed,
            "total_errors": global_vars.total_errors,
        }
    elif report_type == "classify-images":
        report_entry = {
            "timestamp": start_time,
            "report_type": report_type,
            "new_classes_created": global_vars.new_classes_created,
            "new_class_images": global_vars.new_class_images
        }

    reports = []
    if os.path.exists(config.REPORTS_JSON_PATH):
        with open(config.REPORTS_JSON_PATH, 'r') as report_file:
            try:
                reports = json.load(report_file)
            except json.JSONDecodeError:
                reports = []

    reports.append(report_entry)
    
    with open(config.REPORTS_JSON_PATH, 'w') as report_file:
        json.dump(reports, report_file, indent=4)
