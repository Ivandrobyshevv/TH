import time

import requests
from bs4 import BeautifulSoup

from service.parser.Armani.ArmaniParserPage import ArmaniParserPage


class ArmaniParserCard(ArmaniParserPage):

    async def start_parser_card(self):
        links = await self.start()
        used_links = list()
        for card_link in links:
            used_links.append(card_link)
            time.sleep(0.3)
            print(f'Просмотрено {len(used_links)} осталось {len(links) - len(used_links)}')
            try:
                print(f'Получаем информацию с карточки {card_link}\n')
                soup = await self.__get_object_soup(card_link)
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

    async def __get_object_soup(self, url):
        r = requests.get(url=url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
