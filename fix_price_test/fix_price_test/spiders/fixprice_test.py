import scrapy
import datetime
import json


class FixpriceTestSpider(scrapy.Spider):
    name = "fixprice_test"
    allowed_domains = ["fixprice.com"]
    start_urls = ["https://fixprice.com"]

    def parse(self, response):
        # Получаем все категории
        categories = response.xpath('//*[@class="category-tree"]/div').getall()

        for category_url in categories:
            yield response.follow(category_url, callback=self.parse_category)

    def parse_category(self, response):
        # Получаем название категории
        category_name = response.xpath('//h1[@class="page-title"]/text()').get()

        # Получаем информацию о товарах
        products = response.xpath('//*[@class=product xh-highlight"]')
        for product in products:
            # Получаем ссылку на товар
            product_url = product.xpath('//a[@class="title"]').get()

            # Переходим на страницу товара
            yield response.follow(product_url, callback=self.parse_product, meta={'category': category_name})

        # Переходим на следующую страницу категории, если она есть
        next_page_url = response.xpath('//*[@class="pagination"]').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_category)

    def parse_product(self, response):
        # Извлекаем данные о товаре
        timestamp = int(datetime.datetime.now().timestamp())
        rpc = response.xpath('//div[@class="additional-information"]/text()').re_first(r'.*\((.*)\)')
        url = response.url
        title = response.xpath('//h1[@class="title"]/text()').get()

        marketing_tags = response.xpath('//div[@class="wrapper sticker"]/text()').getall()
        brand = response.xpath('//*[@class="value"]//a/text()').get()
        section = response.xpath('//*[@class="category-tree"]/div/text()').getall()

        # Цена
        current_price = response.xpath('//*[@class="special-price"]/text()').re_first(r'(\d+\.\d+)')
        original_price = response.xpath('//*[@class="regular-price old-price"]/text()').re_first(r'(\d+\.\d+)')
        sale_tag = None
        if original_price and float(original_price) > float(current_price):
            discount_percentage = round((float(original_price) - float(current_price)) * 100 / float(original_price))
            sale_tag = f"Скидка {discount_percentage}%"

        # Изображения
        main_image = response.xpath('//img[@class="swiper-lazy swiper-lazy-loaded"]/@src').get()
        set_images = response.xpath('//a[contains(@href, "image")]/img/@src').getall()

        # Метаданные
        metadata = {}
        metadata['__description'] = response.xpath('//div[@class="description"]//text()').get()

        # Создание словаря с данными товара
        product_data = {
            "timestamp": timestamp,
            "RPC": rpc,
            "url": url,
            "title": title,
            "marketing_tags": marketing_tags,
            "brand": brand,
            "section": section,
            "current": float(current_price) if current_price else None,
            "original": float(original_price) if original_price else None,
            "sale_tag": sale_tag,
            "main_image": main_image,
            "set_images": set_images,
            "metadata": metadata
        }


        # Сохранение данных в файл
        with open('fixprice_data.json', 'a') as f:
            json.dump(product_data, f, indent=3)
