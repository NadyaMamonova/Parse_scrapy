#**Используя фреймворк Scrapy необходимо написать парсер для получения информации о товарах интернет-магазина из списка категорий по заранее заданному шаблону**

Данную информацию необходимо представлять в виде списка словарей (один товар - один словарь) и сохранять в файл с расширением .json

На вход подается список категорий (минимум 3), с количеством товаров от 70 штук на категорию (более 3 страниц в одной категории) 
на сайте fix-price.com (Например: https://fix-price.com/catalog/kosmetika-i-gigiena/ukhod-za-polostyu-rta)

Обязательно осуществлять сбор данных с учетом выбранного региона для парсинга - Екатеринбург

По возможности для получения информации добавить использование подключения через прокси

Формат выходных данных для одного товара:

{

    "timestamp": int,  # Дата и время сбора товара в формате timestamp.
    "RPC": "str",  # Уникальный код товара.
    "url": "str",  # Ссылка на страницу товара.
    "title": "str",  # Заголовок/название товара (! Если в карточке товара указан цвет или объем, но их нет в названии, необходимо добавить их в title в формате: "{Название}, {Цвет или Объем}").
    "marketing_tags": ["str"],  # Список маркетинговых тэгов, например: ['Популярный', 'Акция', 'Подарок']. Если тэг представлен в виде изображения собирать его не нужно.
    "brand": "str",  # Бренд товара.
    "section": ["str"],  # Иерархия разделов, например: ['Игрушки', 'Развивающие и интерактивные игрушки', 'Интерактивные игрушки'].
    "price_data": {
        "current": float,  # Цена со скидкой, если скидки нет то = original.
        "original": float,  # Оригинальная цена.
        "sale_tag": "str"  # Если есть скидка на товар то необходимо вычислить процент скидки и записать формате: "Скидка {discount_percentage}%".
    },
    "stock": {
        "in_stock": bool,  # Есть товар в наличии в магазине или нет.
        "count": int  # Если есть возможность получить информацию о количестве оставшегося товара в наличии, иначе 0.
    },
    "assets": {
        "main_image": "str",  # Ссылка на основное изображение товара.
        "set_images": ["str"],  # Список ссылок на все изображения товара.
        "view360": ["str"],  # Список ссылок на изображения в формате 360.
        "video": ["str"]  # Список ссылок на видео/видеообложки товара.
    },
    "metadata": {
        "__description": "str",  # Описание товара
        "KEY": "str",
        "KEY": "str",
        "KEY": "str"
        # Также в metadata необходимо добавить все характеристики товара которые могут быть на странице.
        # Например: Артикул, Код товара, Цвет, Объем, Страна производитель и т.д.
        # Где KEY - наименование характеристики.
    }
    "variants": int,  # Кол-во вариантов у товара в карточке (За вариант считать только цвет или объем/масса. Размер у одежды или обуви варинтами не считаются).

}


##**Установить зависимости**


pip install scrapy


##**Запуск**


scrapy crawl fixprice_test -o fixprice_data.json
