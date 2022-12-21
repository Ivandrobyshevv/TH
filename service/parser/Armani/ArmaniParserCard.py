import logging
import time

from service.parser.Armani.ArmaniParser import ArmaniParser


class ArmaniParserCard(ArmaniParser):
    def __int__(self, base_url, headers):
        super().__int__(base_url, headers)

    def start(self):
        total_product = 0
        total_link_card = list()
        categories = {"Man": "/men/view-all-sale-man", "Woman": "/women/view-all-sale-woman"}
        for key, value in categories.items():
            logging.info(f"Начало сбора данных со страницы Армани р в категории {key}")
            amount_product, amount_link_card = self.open_url(self._ArmaniParser__generator_url(value), key)
            total_product += amount_product
            total_link_card += amount_link_card
        self.__parsing_all_item_on_page(total_product, total_link_card)

    def __parsing_all_item_on_page(self, total_prod, link_cards):
        used_links = list()
        for card_link in link_cards:
            used_links.append(card_link)
            time.sleep(0.3)
            print(f'Просмотрено {len(used_links)} осталось {total_prod - len(used_links)}')
            try:
                print(f'Получаем информацию с карточки {card_link}\n')
                soup = self.get_object_soup(card_link)
                title = soup.find("h1", class_="item-info__item-name").text.strip()
                link = card_link
                old_price = soup.find("span", class_="full").text.strip().split("\n")[-1]
                new_price = soup.find("span", class_="discounted").text.strip().split("\n")[-1]
                images = []
                all_images = soup.find_all("li", class_="item-image")
                for image in all_images:
                    images.append(image.find("img").get("src"))
                print(f'title: {title}\nlink:{link}\nold_price: {old_price}\nnew_price:{new_price}\nimages: {images}')
            except Exception as e:
                print(e)
                continue
