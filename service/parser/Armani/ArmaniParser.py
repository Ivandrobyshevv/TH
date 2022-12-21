from bs4 import BeautifulSoup

from service.parser.Armani.Parser import BaseParser


class ArmaniParser(BaseParser):

    def __init__(self, base_url: str, headers: dict):
        super().__init__(base_url, headers)
        self.cat = None

    @staticmethod
    def get_amount_page(soup: BeautifulSoup) -> str:
        """Парсинг кол-во страниц на сайта"""
        amount_page = soup.find("div", class_="pagination__info").text.strip().split(" ")[-1]
        return amount_page

    def get_all_link_cards(self, url: str):
        all_links = []
        """Получение всех ссылок на карточки товара"""
        soup = self.get_object_soup(url)
        value = soup.find("section", class_="product-list").find_all("div", class_="item-card__variant")
        for _ in value:
            if not _.find("a", class_="item-card__pdp-link-image").get("href") in all_links:
                all_links.append(_.find("a", class_="item-card__pdp-link-image").get("href"))
            else:
                continue
        return all_links

    def open_url(self, url: str, name_cat: str) -> (int, list):
        print(f"Сбор информации с категории {name_cat}")
        links_card = []
        soup = self.get_object_soup(url)
        pages = self.get_amount_page(soup)  # Кол-во страниц

        for page in range(1, int(pages) + 1):
            url_page = f'{url}?page={page}'
            print(f'Получение информации с {url_page}')
            links_card += self.get_all_link_cards(url_page)

        total_prod = len(links_card)

        return total_prod, links_card

    def __generator_url(self, category) -> str:
        return f"{self.base_url}{category}"
