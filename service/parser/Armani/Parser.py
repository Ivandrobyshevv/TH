import abc

import requests
from bs4 import BeautifulSoup


class BaseParser:
    def __init__(self, base_url: str, headers: dict) -> None:
        self.base_url = base_url
        self.headers = headers

    @abc.abstractmethod
    def open_url(self, url: str):
        pass

    def get_object_soup(self, url: str) -> BeautifulSoup:
        """Получение объекта BeautifulSoup"""
        try:
            r = requests.get(url=url, headers=self.headers)
            soup = BeautifulSoup(r.content, 'lxml')
            return soup
        except Exception as e:
            print(f'Проверьте ссылку: {url} - {e}')


