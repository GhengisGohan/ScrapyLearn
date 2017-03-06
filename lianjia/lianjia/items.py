# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    rental = scrapy.Field()
    distance = scrapy.Field()
    area = scrapy.Field()
    room_number = scrapy.Field()
    direction = scrapy.Field()
    year_build = scrapy.Field()

    pass
