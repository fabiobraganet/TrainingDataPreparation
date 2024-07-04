import os
import logging
import asyncio
from modules import classification, report, startup
from utils import config
from datetime import datetime
import global_vars

async def main():
    loop = asyncio.get_running_loop()
    logging.info(f"Main loop: {loop}")
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    await startup.run(start_time)

    if not os.path.exists(config.RESIZED_IMAGES_DIR):
        logging.info("Sem imagens redimensionadas para classificar")
        return

    await classification.run(start_time)

    report.finalize_report("resize-images", start_time)
    report.finalize_report("classify-images", start_time)

if __name__ == "__main__":
    logging.basicConfig(level=logging.FATAL)
    asyncio.run(main())
