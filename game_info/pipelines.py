# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import codecs
import game_info.spiders.gameInfoSpider as gameInfoSpider

class GameInfoPipeline(object):
    def process_item(self, item, spider):
        line = u'<li><a href=\"{0}\">{1}</a><p>{2}</p></li>\n'.format(item['url'], item['title'], item['content'])
        self.file.write(line)

    def open_spider(self, spider):
        print 'open spider', spider.name
        self.file = codecs.open('log/%s/items_%s.html' % (sys.argv[1], spider.name), 'w+', encoding='utf-8')

    def close_spider(self, spider):
        print 'close spider', spider.name
        self.file.close()