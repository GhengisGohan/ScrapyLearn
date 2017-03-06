# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FenciPipeline(object):

    def process_item(self, item, spider):
        content = item['content'].encode('utf-8')
        if content:
            f = open('mimeng.txt', 'a')
            f.writelines(content)
            f.close()
        return item
