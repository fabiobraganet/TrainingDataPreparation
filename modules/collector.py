import aiohttp
import asyncio
import logging

class Collector:
    def __init__(self, max_connections):
        self.sem = asyncio.Semaphore(max_connections)
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120))  

    async def fetch_image(self, url):
        loop = asyncio.get_running_loop()
        logging.info(f"Fetch loop: {loop}")
        async with self.sem:
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        logging.info(f"Iniciando leitura da imagem da URL {url}")
                        data = await response.read()
                        logging.info(f"Imagem coletada com sucesso da URL {url}, tamanho: {len(data)} bytes")
                        return data
                    else:
                        logging.error(f"Erro ao coletar imagem da URL {url}: {response.status}")
                        return None
            except Exception as e:
                logging.error(f"Erro ao coletar imagem da URL {url}: {e}")
                return None

    async def collect_images(self, urls):
        loop = asyncio.get_running_loop()
        logging.info(f"Collect loop: {loop}")
        tasks = [self.fetch_image(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logging.error(f"Erro durante a coleta da imagem da URL {urls[i]}: {result}")
                results[i] = None
        return results

    async def close(self):
        await self.session.close()
