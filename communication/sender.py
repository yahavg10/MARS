import logging
from typing import Dict, Callable, NoReturn

import aiohttp as aiohttp
import requests
from requests import RequestException

from utils.variables_utils import suffixes, file_read_mode
from utils.wrapper import wrap_callable

logger = logging.getLogger(name="finals_logger")


class Sender:
    toolbox: Dict[str, Callable] = {}

    def __init__(self, create_payload_fn: Callable):
        self.create_payload = wrap_callable(create_payload_fn, ())

    def send_request(self, url: str, folder_path: str, common_name: str, method: str = 'POST') -> NoReturn:
        payload = self.create_payload(folder_path, common_name, suffixes, file_read_mode)
        try:
            logger.info(f"Sending {method} request to {url} with payload: {payload}")
            response = requests.post(url=url, files=payload)
            logger.info(response.json())
        except RequestException as e:
            logger.error(f"Error during request: {str(e)}")
