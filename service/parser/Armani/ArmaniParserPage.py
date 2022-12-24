import logging
import time

from service.parser.Armani.ArmaniParser import ArmaniParser


class ArmaniParserPage(ArmaniParser):
    def __int__(self, base_url, headers):
        super().__int__(base_url, headers)

    async def start(self):
        url_cards = list()
        categories = {"Man": "/men/view-all-sale-man", "Woman": "/women/view-all-sale-woman"}
        for cat_name, url_cat in categories.items():
            total_product, total_page, all_card, current_page = await self.open_url(await self.__generator_url(url_cat))
            url_cards.extend(await self.__get_all_link_cards(all_card))
            if int(total_page) > 1:
                for page in range(2, int(total_page) + 1):
                    total_item = await self.open_url(
                        await self.__generator_url(url_cat, page))
                    all_card = total_item[2]
                    url_cards.extend(await self.__get_all_link_cards(all_card))
                    print(f"Получено карточек: {len(url_cards)}")
        return url_cards

    # def __parsing_all_item_on_page(self, total_prod, link_cards):
    #     used_links = list()
    #     for card_link in link_cards:
    #         used_links.append(card_link)
    #         time.sleep(0.3)
    #         print(f'Просмотрено {len(used_links)} осталось {total_prod - len(used_links)}')
    #         try:
    #             print(f'Получаем информацию с карточки {card_link}\n')
    #             soup = self.get_object_soup(card_link)
    #             title = soup.find("h1", class_="item-info__item-name").text.strip()
    #             link = card_link
    #             old_price = soup.find("span", class_="full").text.strip().split("\n")[-1]
    #             new_price = soup.find("span", class_="discounted").text.strip().split("\n")[-1]
    #             images = []
    #             all_images = soup.find_all("li", class_="item-image")
    #             for image in all_images:
    #                 images.append(image.find("img").get("src"))
    #             print(f'title: {title}\nlink:{link}\nold_price: {old_price}\nnew_price:{new_price}\nimages: {images}')
    #         except Exception as e:
    #             print(e)
    #             continue

    @staticmethod
    async def __get_all_link_cards(all_card):
        all_links = []
        """Получение всех ссылок на карточки товара"""
        for _ in all_card:
            if not _.find("a", class_="item-card__pdp-link-image").get("href") in all_links:
                all_links.append(_.find("a", class_="item-card__pdp-link-image").get("href"))
            else:
                continue
        return all_links

    async def __generator_url(self, url_cat: str, page=None) -> str:
        if page is not None:
            return f'{self.base_url}{url_cat}?page={page}'
        else:
            return f'{self.base_url}{url_cat}'
