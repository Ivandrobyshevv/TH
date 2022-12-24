import abc

import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, base_url: str, headers: dict) -> None:
        self.base_url = base_url
        self.headers = headers

    @abc.abstractmethod
    async def open_url(self, url: str):
        pass


