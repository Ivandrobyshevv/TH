import requests
from bs4 import BeautifulSoup

from service.parser.Parser import Parser


class ArmaniParser(Parser):

    def __init__(self, base_url: str, headers: dict):
        super().__init__(base_url, headers)

    async def start(self):
        await self.open_url(self.base_url)

    # @staticmethod
    # def get_amount_page(soup: BeautifulSoup) -> str:
    #     """Парсинг кол-во страниц на сайта"""
    #     amount_page = soup.find("div", class_="pagination__info").text.strip().split(" ")[-1]
    #     return amount_page

    # def get_all_link_cards(self, url: str):
    #     all_links = []
    #     """Получение всех ссылок на карточки товара"""
    #     soup = self.get_object_soup(url)
    #     value = soup.find("section", class_="product-list").find_all("div", class_="item-card__variant")
    #     for _ in value:
    #         if not _.find("a", class_="item-card__pdp-link-image").get("href") in all_links:
    #             all_links.append(_.find("a", class_="item-card__pdp-link-image").get("href"))
    #         else:
    #             continue
    #     return all_links

    async def open_url(self, url: str):
        try:
            r = requests.get(url=url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'lxml')
            print(f"Открыли страницу {url}")
        except Exception as e:
            print(e)

        try:
            total_product = soup.find(class_="totalResults").text.strip().split(" ")[0]
            total_page = soup.find("div", class_="pagination__info").text.strip().split(" ")[-1]
        except:
            total_product = 0
            total_page = 0

        all_card = soup.find("section", class_="product-list").find_all("div", class_="item-card__variant")
        current_page = soup.find("ul", class_="pagination__list").find(class_="pagination__item--current").text.strip()
        print(
            f'Текущая страница: {current_page}\n'
            f'Всего страниц в категории: {total_page}\n'
            f'Всего товаров: {total_product}\n'
        )

        return total_product, total_page, all_card, current_page

    # def __generator_url(self, category) -> str:
    #     return f"{self.base_url}{category}"
