# -*- coding: utf-8 -*-

import sys
import datetime
from scrapy.selector import Selector
from scrapy.http import  Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from game_info.items import GameInfoItem

spider_date = datetime.datetime.strptime(sys.argv[1], '%Y%m%d')
s1 = spider_date.strftime('%m%d%Y') # 10202016
s2 = spider_date.strftime('%Y-%m-%d') # 2016-10-20
s3 = spider_date.strftime('%y%m') # 1610
s4 = spider_date.strftime('%Y%m%d') # 20161020
s5 = spider_date.strftime('%Y%m') # 201610
s6 = spider_date.strftime('%y/%m%d') # 16/1020
s7 = spider_date.strftime('%y%m%d') # 161020
s8 = spider_date.strftime('%Y-%m') # 2016-10
s9 = spider_date.strftime('%Y/%m') # 2016/10
s10 = spider_date.strftime('%y-%m-%d') # 16-10-20
s11 = spider_date.strftime('%m-%d') # 10-20
s12 = spider_date.strftime('%Y年%m月%d日').decode('utf-8') #2016年10月24日
s13 = spider_date.strftime('%Y') # 2016

def global_parse_content(response, div_path=''):
    print 'hh', response.url

    content_xpath = u'//div%s//p[ \
        ((contains(text(), "妖尾") or contains(text(), "妖精的尾巴") or contains(text(), "妖精尾巴") or contains(text(), "魔导少年")) \
        and (contains(text(), "IP") or contains(text(), "手游") or contains(text(), "改编") or contains(text(), "授权") or contains(text(), "中国") or contains(text(), "大陆"))) \
        or (contains(translate(text(), "FPS+MOBA", "fps+moba"), "fps+moba")) \
        or (contains(text(), "守望先锋") and contains(text(), "手游")) \
        or (contains(text(), "王者军团")) \
        or (contains(text(), "特攻先锋")) \
        or (contains(text(), "枪火") or contains(text(), "枪火游侠")) \
        ]//text()' % (div_path)

    sel = Selector(response)
    content = sel.xpath(content_xpath)
    
    if len(content) > 0:
        print 'get content'
        item = GameInfoItem()
        item['url'] = response.url
        item['title'] = sel.xpath('//title/text()').extract_first()
        item['content'] = content.extract_first()
        return item

class s17173Spider(CrawlSpider):
    # name of spiders
    name = 's17173Spider'
    allowed_domains = ['17173.com']
    start_urls = [
        'http://www.17173.com',
        'http://news.17173.com/',
        'http://newgame.17173.com/',
        'http://news.17173.com/dalu/',
        'http://news.17173.com/quanqiu/',
        'http://news.17173.com/chanye/list.shtml',
        'http://newgame.17173.com/game-newslist.html',
        'http://newgame.17173.com/game-demolist.html',
    ]
    rules = [
        #http://news.17173.com/content/10132016/160912434.shtml ok
        #http://news.17173.com/content/2016-09-18/20160918154038916.shtml ok
        #http://newgame.17173.com/news/10112016/101540273_1.shtml ok
        Rule(LinkExtractor(allow=('news.17173.com/content/' + s1 + '/\w+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('news.17173.com/content/' + s2 + '/\w+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('newgame.17173.com/news/' + s1 + '/\w+\.shtml$')), callback='parse_content', follow=True),
    ]

    # news <div class="gb-final-mod-info"><span class="gb-final-date">2016-10-13 16:09:12</span>
    # newgame <div class="info"><span class="col-01">2016-10-11 10:15:40</span>
    def parse_content(self, response):
        item = global_parse_content(response)
        if item is not None:
            yield item

class sduowanSpider(CrawlSpider):
    name = 'sduowanSpider'
    allowed_domains = ['duowan.com']
    start_urls = [
        'http://www.duowan.com',
        'http://news.duowan.com/',
        'http://news.duowan.com/1410/m_276866157894_2.html',
        'http://newgame.duowan.com/',
        'http://newgame.duowan.com/1507/m_300968157763.html'
    ]
    rules = [
        #http://www.duowan.com/1610/340301585593.html ok
        #http://news.duowan.com/1610/340279015237.html ok
        #http://newgame.duowan.com/1610/340055564665.html ok
        #http://ps4.duowan.com/1610/340304594896.html no
        #http://3ds.duowan.com/1610/340304594896.html no
        #http://psv.duowan.com/1610/340304594896.html no
        #http://vrgame.duowan.com/1610/340287388551.html no
        Rule(LinkExtractor(allow=('news.duowan.com/' + s3 + '/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.duowan.com/' + s3 + '/\d+\.html$')), callback='parse_content2', follow=True),
        Rule(LinkExtractor(allow=('newgame.duowan.com/' + s3 + '/\d+\.html$')), callback='parse_content2', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # news <address class="news-post__meta"><span class="news-post__meta-item">时间：2016-10-13 09:56:55</span>
        if len(sel.xpath(u'//span[@class="news-post__meta-item" and contains(text(), "时间：' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

    def parse_content2(self, response):
        sel = Selector(response)
        # www <div class="newsDetail-header__info"><span>发表时间：<em>2016-10-13 16:16:06</em></span>
        # www <address>[<span>发表时间：2016-09-28 10:35:43</span><span>发表来源：多玩</span><span>作者：阿抖猫</span>]
        # newgame <div class="newsDetail-header__info"><span>[<span>发表时间：<em>2016-10-21 18:25:30</em></span>
        # newgame <address>[<span>发表时间：2016-05-17 09:30:23</span><span>发表来源：多玩</span><span>作者：言心</span>]
        if len(sel.xpath(u'//span[contains(text(), "发表时间：' + s2 
            + u'") or contains(text(), "发表时间：<em>' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class s5253Spider(CrawlSpider):
    name = 's5253Spider'
    allowed_domains = ['5253.com']
    start_urls = ['http://www.5253.com']
    rules = [
        #http://www.5253.com/articles/316830.html ok
        Rule(LinkExtractor(allow=('www.5253.com/articles/\d+\.html$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # 5253 <span class="time">2016-10-22 11:27</span>
        if len(sel.xpath('//span[contains(@class, "time") and contains(text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class sqqSpider(CrawlSpider):
    name = 'sqqSpider'
    allowed_domains = ['qq.com']
    start_urls = [
        'http://games.qq.com',
        'http://games.qq.com/newgames/',
        'http://games.qq.com/mobile/',
    ]
    rules = [
        #http://games.qq.com/a/20161013/019028.htm ok
        Rule(LinkExtractor(allow=('games.qq.com/a/' + s4 + '/\d+\.htm')), callback='parse_content', follow=True),
    ]

    # <span class="article-time">2016-10-13 10:16</span>
    def parse_content(self, response):
        item = global_parse_content(response)
        if item is not None:
            yield item

class ssinaSpider(CrawlSpider):
    name = 'ssinaSpider'
    allowed_domains = ['sina.com.cn']
    start_urls = [
        'http://games.sina.com.cn',
        'http://games.sina.com.cn/newgame/',
        'http://games.sina.com.cn/y/',
        'http://games.sina.cn/pc/newslist.d.html?addstr=35435,35437,174618&page=1&pagesize=100',
        'http://games.sina.cn/pc/newslist.d.html?addstr=6764,6765,6767,6768,6769,152046,152047&page=1&pagesize=100',
    ]
    rules = [
        #http://games.sina.com.cn/t/n/2016-10-13/fxwvpar7913096.shtml ok
        #http://games.sina.com.cn/ol/n/2016-10-13/fxwvpar7916088.shtml ok
        Rule(LinkExtractor(allow=('games.sina.com.cn/.*/' + s2 + '/\w+\.shtml$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        item = global_parse_content(response)
        if item is not None:
            yield item

class s97973Spider(CrawlSpider):
    name = 's97973Spider'
    allowed_domains = ['97973.com']
    start_urls = [
        'http://www.97973.com',
        'http://www.97973.com/ios/news.shtml',
        'http://www.97973.com/android/news.shtml',
        'http://www.97973.com/ios/industry.shtml',
        'http://www.97973.com/android/industry.shtml',
    ]
    rules = [
        #http://www.97973.com/moxw/2016-10-22/ifxwztrt0119972.shtml ok
        Rule(LinkExtractor(allow=('www.97973.com/(moxw|sjyj)/' + s2 + '/\w+\.shtml$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        item = global_parse_content(response, '[@class="LEFT"]')
        if item is not None:
            yield item

class suuu9Spider(CrawlSpider):
    name = 'suuu9Spider'
    allowed_domains = ['uuu9.com']
    start_urls = [
        'http://www.uuu9.com/',
        'http://news.uuu9.com/',
        'http://newgame.uuu9.com/',
    ]
    rules = [
        #http://news.uuu9.com/china/201610/395727.shtml ok
        #http://news.uuu9.com/rihan/201608/392530.shtml ok
        #http://news.uuu9.com/oumei/201603/381718.shtml ok
        #http://newgame.uuu9.com/2016/201606/389561.shtml ok
        Rule(LinkExtractor(allow=('news.uuu9.com/[A-Za-z]+/' + s5 + '/\d+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('newgame.uuu9.com/' + s13 + '/' + s5 + '/\d+\.shtml$')), callback='parse_content2', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # <div class="cl index_content"><h4><em></em>2016-8-10 10:34:45  作者:佚名 来源:腾讯游戏</h4>
        if len(sel.xpath(u'//div[@class="cl index_content" and contains(string(.), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

    def parse_content2(self, response):
        sel = Selector(response)
        # <p class="texttop cl"><span class="l">2016-06-30 来源：网络 作者：未知</span>
        if len(sel.xpath(u'//span[@class="l" and contains(text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class syoyojieSpider(CrawlSpider):
    name = 'syoyojieSpider'
    allowed_domains = ['yoyojie.com']
    start_urls = [
        'http://www.yoyojie.com',
        'http://www.yoyojie.com/news/',
        'http://www.yoyojie.com/news/hangye/1.shtml',
        'http://www.yoyojie.com/news/hangye/2.shtml',
        'http://www.yoyojie.com/news/xinyou/1.shtml',
        'http://www.yoyojie.com/news/xinyou/2.shtml',
        'http://www.yoyojie.com/news/chanye/1.shtml',
        'http://www.yoyojie.com/news/chanye/2.shtml',
        'http://www.yoyojie.com/syzx/1.shtml',
        'http://www.yoyojie.com/syzx/2.shtml',
    ]
    rules = [
        #http://www.yoyojie.com/syzx/20161013/234290.shtml ok
        #http://www.yoyojie.com/news/hangye/20161019/234767.shtml ok
        #http://www.yoyojie.com/pingce/20161013/234271.shtml no
        #http://www.yoyojie.com/gonglue/20150907/195621.shtml no
        Rule(LinkExtractor(allow=('www.yoyojie.com/syzx/' + s4 + '/\d+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.yoyojie.com/news/(hangye|xinyou|chanye)/' + s4 + '/\d+\.shtml$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        item = global_parse_content(response)
        if item is not None:
            yield item

class spcgamesSpider(CrawlSpider):
    name = 'spcgamesSpider'
    allowed_domains = ['pcgames.com.cn']
    start_urls = [
        'http://www.pcgames.com.cn',
        'http://news.pcgames.com.cn/',
        'http://ng.pcgames.com.cn/',
        'http://ng.pcgames.com.cn/xyxw/',
        'http://sy.pcgames.com.cn/',
        'http://sy.pcgames.com.cn/news/',
        'http://sy.pcgames.com.cn/news/fnews/',
        'http://sy.pcgames.com.cn/news/inews/',
        'http://sy.pcgames.com.cn/zixun/',
        'http://wangyou.pcgames.com.cn/',
        'http://wangyou.pcgames.com.cn/xwkx/',
        'http://wangyou.pcgames.com.cn/xwkx/gnww/',
    ]
    rules = [
        #http://news.pcgames.com.cn/638/6388759.html ok
        #http://ng.pcgames.com.cn/618/6180594.html ok
        #http://sy.pcgames.com.cn/641/6411033.html ok
        #http://wangyou.pcgames.com.cn/641/6410234.html yes
        #http://pc.pcgames.com.cn/638/6382902.html no
        #http://web.pcgames.com.cn/641/6413032.html no
        #http://fight.pcgames.com.cn/641/6413012.html no

        #news <div class="box-bd box-bdn new">
        #ng <div id="topnewsContent" class="topnews-content"> <div class="focus-box focus-news">
        #sy <div id="topnewsContent" class="topnews-content">
        #wangyou <div id="topnewsContent" class="topnews-content"> <div class="focus-box focus-news" style="display: block;">
        Rule(LinkExtractor(allow=('news.pcgames.com.cn/\d+/\d+\.html$'), restrict_xpaths='//div[@class="box-bd box-bdn new"]'), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('ng.pcgames.com.cn/\d+/\d+\.html$'), restrict_xpaths='//div[@class="topnews-content" or @class="focus-box focus-news"]'), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('sy.pcgames.com.cn/\d+/\d+\.html$'), restrict_xpaths='//div[@class="topnews-content" or @class="focus-box focus-news"]'), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('wangyou.pcgames.com.cn/\d+/\d+\.html$'), restrict_xpaths='//div[@class="topnews-content" or @class="focus-box focus-news"]'), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # <div class="article-info"><span class="article-info-date">2016-10-02 16:42</span>
        if len(sel.xpath(u'//div[@class="article-info" and contains(span[@class="article-info-date"]/text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item
        
class stgbusSpider(CrawlSpider):
    name = 'stgbusSpider'
    allowed_domains = ['tgbus.com']
    start_urls = [
        'http://www.tgbus.com',
        'http://ol.tgbus.com',
        'http://shouji.tgbus.com',
    ]
    rules = [
        #http://shouji.tgbus.com/201610/9840495168.html ok
        #http://ol.tgbus.com/201610/2477395997.html ok 
        #http://ps4.tgbus.com/news/201610/20161013103730.shtml no
        #http://3ds.tgbus.com/news/newslist/201610/20161011134535.shtml no
        #http://xbox360.tgbus.com/zixun/yenei/201610/20161005144443.shtml no
        Rule(LinkExtractor(allow=('shouji.tgbus.com/' + s5 + '/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('ol.tgbus.com/' + s5 + '/\d+\.html$')), callback='parse_content', follow=True),
    ]
    
    def parse_content(self, response):
        sel = Selector(response)
        # <div class="author-item"><div class="time">2016-10-23</div>
        if len(sel.xpath(u'//div[@class="author-item" and contains(div[@class="time"]/text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class s163Spider(CrawlSpider):
    name = 's163Spider'
    allowed_domains = ['163.com']
    start_urls = [
        'http://play.163.com',
        'http://play.163.com/shouyou/',
        'http://play.163.com/xin/',
    ]
    rules = [
        #http://play.163.com/16/1013/12/C38PO79P00314OSE.html ok
        #http://play.163.com/16/1013/17/C39AN9DI00314J6L.html ok
        Rule(LinkExtractor(allow=('play.163.com/' + s6 + '/\d+/\w+\.html$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        item = global_parse_content(response)
        if item is not None:
            yield item       

class s178Spider(CrawlSpider):
    name = 's178Spider'
    allowed_domains = ['178.com']
    start_urls = [
        'http://www.178.com',
        'http://news.178.com/',
        'http://news.178.com/list/242375821947.html',
        'http://news.178.com/list/233371578701.html'
        'http://news.178.com/list/233371578701_2.html',
        'http://news.178.com/list/chanye.html',
        'http://shouyou.178.com/',
        'http://xin.178.com/',
        'http://xin.178.com/list/zzd/index.html',
        'http://xin.178.com/list/33074608704.html',
        'http://xin.178.com/list/33074608704_2.html',
    ]
    rules = [
        #http://news.178.com/201610/270237686264.html ok
        #http://xin.178.com/201610/270345146131.html ok
        #http://shouyou.178.com/201610/2433295991.html ok
        Rule(LinkExtractor(allow=('news.178.com/' + s5 + '/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('xin.178.com/' + s5 + '/\d+\.html$')), callback='parse_content2', follow=True),
        Rule(LinkExtractor(allow=('shouyou.178.com/' + s5 + '/\d+\.html$')), callback='parse_content3', follow=True),
    ]
    
    def parse_content(self, response):
        sel = Selector(response)
        # news <div id="content-header"><p id="content-meta">2016-10-21 13:58:57</p> </div>
        if len(sel.xpath(u'//div[@id="content-header" and contains(p[@id="content-meta"]/text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

    def parse_content2(self, response):
        sel = Selector(response)
        # xin <div id="contentTitle"><p class="colorGray"><span id="publicDate">发布日期：2016-10-13</span>
        if len(sel.xpath(u'//div[@id="contentTitle" and contains(p/span[@id="publicDate"]/text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

    def parse_content3(self, response):
        sel = Selector(response)
        # shouyou <div class="author-item"><div class="time">2016-10-13</div></div>
        if len(sel.xpath(u'//div[@id="author-item" and contains(//div[@id="time"]/text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item
        
class syouxiduoSpider(CrawlSpider):
    name = 'syouxiduoSpider'
    allowed_domains = ['youxiduo.com']
    start_urls = [
        'http://www.youxiduo.com',
        'http://www.youxiduo.com/zixun/',
        'http://www.youxiduo.com/zixun/?startsize=1&oldsize=10&page=2',
        'http://www.youxiduo.com/zixun/?startsize=1&oldsize=10&page=3',
        'http://www.youxiduo.com/zixun/?startsize=1&oldsize=10&page=4',
        'http://www.youxiduo.com/zixun/?startsize=1&oldsize=10&page=5',
        'http://www.youxiduo.com/xinyou/',
        'http://www.youxiduo.com/industry/',
    ]
    rules = [
        #http://www.youxiduo.com/content/tTHySVXECRwF.html ok
        Rule(LinkExtractor(allow=('www.youxiduo.com/content/.*\.html$'), restrict_xpaths='//div[@class="listLt" or @class="topLine"]'), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        #<div class="contentTitle"><p><span>2016-10-21 19:51</span>
        if len(sel.xpath(u'//div[@class="contentTitle" and contains(p/span/text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item
        
class sgamerskySpider(CrawlSpider):
    name = 'sgamerskySpider'
    allowed_domains = ['gamersky.com']
    start_urls = [
        'http://www.gamersky.com',
        'http://www.gamersky.com/news/',
        'http://shouyou.gamersky.com',
        'http://shouyou.gamersky.com/zx/',
        'http://ol.gamersky.com',
    ]
    rules = [
        #http://www.gamersky.com/news/201610/818775.shtml ok
        #http://shouyou.gamersky.com/news/201610/820649.shtml ok
        #http://ol.gamersky.com/news/201610/820636.shtml ok
        Rule(LinkExtractor(allow=('www.gamersky.com/news/' + s5 + '/\d+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('shouyou.gamersky.com/news/' + s5 + '/\d+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('ol.gamersky.com/news/' + s5 + '/\d+\.shtml$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # <div class="Mid2L_tit"><div class="detail">2016-10-23 09:27:07
        # shouyou <div class="Mid2L_title"><div class="detail"><span class="txt">2016-10-14 10:54:05</span>
        if len(sel.xpath(u'//div[@class="detail" and contains(string(.), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class sali213Spider(CrawlSpider):
    name = 'sali213Spider'
    allowed_domains = ['ali213.net']
    start_urls = [
        'http://www.ali213.net',
        'http://www.ali213.net/news/',
        'http://www.ali213.net/news/game/',
        'http://www.ali213.net/news/game/index_2.html',
        'http://www.ali213.net/news/game/index_3.html',
        'http://www.ali213.net/news/game/index_4.html',
        'http://www.ali213.net/news/game/index_5.html',
        'http://www.ali213.net/news/topnews/',
        'http://www.ali213.net/news/topnews/index_2.html',
        'http://m.ali213.net/',
        'http://m.ali213.net/news/',
        'http://m.ali213.net/news/index_2.html',
        'http://m.ali213.net/news/index_3.html',
        'http://m.ali213.net/news/index_4.html',
        'http://m.ali213.net/news/index_5.html',
    ]
    rules = [
        #http://www.ali213.net/news/html/2016-10/254523.html ok
        #http://m.ali213.net/news/161024/64773.html ok
        #http://m.ali213.net/news/161024/gl_64785.html no
        #http://web.ali213.net/news/html/2016-10/325783.html no
        Rule(LinkExtractor(allow=('m.ali213.net/news/' + s7 + '/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.ali213.net/news/html/' + s8 + '/\d+\.html$')), callback='parse_content2', follow=True),
    ]

    def parse_content(self, response):
        item = global_parse_content(response)
        if item is not None:
            yield item

    def parse_content2(self, response):
        sel = Selector(response)
        # <div class="newstag"><div class="newstag_l">2016-10-23 09:26
        if len(sel.xpath(u'//div[@class="newstag_l" and contains(text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item
        
class s3dmgameSpider(CrawlSpider):
    name = 's3dmgameSpider'
    allowed_domains = ['3dmgame.com']
    start_urls = [
        'http://www.3dmgame.com',
        'http://www.3dmgame.com/news/',
        'http://www.3dmgame.com/news/?tid=2&page=2',
        'http://shouyou.3dmgame.com/',
        'http://shouyou.3dmgame.com/news/',
        'http://shouyou.3dmgame.com/news/page_2.html',
        'http://shouyou.3dmgame.com/news/page_3.html',
        'http://shouyou.3dmgame.com/news/page_4.html',
        'http://shouyou.3dmgame.com/news/page_5.html',
    ]
    rules = [
        #http://www.3dmgame.com/news/201610/3598748.html ok
        #http://shouyou.3dmgame.com/news/695.html ok
        #shouyou <div class="Grandson-left-son"><div class="comm-icon"><div class="comm-icon-date">2016-10-21</div>
        Rule(LinkExtractor(allow=('www.3dmgame.com/news/' + s5 + '/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('shouyou.3dmgame.com/news/\d+\.html$'), restrict_xpaths='//div[@class="comm-icon-date" and contains(text(), "' + s2 + '")]/../..'), callback='parse_content2', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # <div class="arctitle"><span><a href="http://www.3dmgame.com/">3dmgame.com</a> 发布时间：2016-10-11 15:52
        if len(sel.xpath(u'//div[@class="arctitle" and contains(string(.), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item
    
    def parse_content2(self, response):
        sel = Selector(response)
        # shouyou <div class="bt_top"><p class="bt_top_time">3dmgame.com 发布时间：2016-10-19 11:45
        if len(sel.xpath(u'//p[@class="bt_top_time" and contains(text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class syzzSpider(CrawlSpider):
    name = 'syzzSpider'
    allowed_domains = ['yzz.cn']
    start_urls = [
        'http://www.yzz.cn',
        'http://news.yzz.cn/',
        'http://news.yzz.cn/new.html',
        'http://sy.yzz.cn/',
        'http://sy.yzz.cn/news/',
        'http://sy.yzz.cn/news/14324-2.shtml',
        'http://sy.yzz.cn/news/14324-3.shtml',
        'http://sy.yzz.cn/news/14324-4.shtml',
        'http://sy.yzz.cn/news/14324-5.shtml',
        'http://sy.yzz.cn/sycyz/cyxw/',
        'http://sy.yzz.cn/sycyz/cyxw/14987-2.shtml',
    ]
    rules = [
        #http://news.yzz.cn/domestic/201610-1018524.shtml ok
        #http://sy.yzz.cn/news/201610-1020406.shtml ok
        #http://sy.yzz.cn/sycyz/cyxw/201610-1018825.shtml ok
        Rule(LinkExtractor(allow=('news.yzz.cn/\w+/' + s5 + '-\d+\.shtml$'), restrict_xpaths='//div[@class="i-news-list" or @class="focus"]'), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('sy.yzz.cn/news/' + s5 + '-\d+\.shtml$'), restrict_xpaths='//div[@class="module g_w350 headline" or @id="pic-txt"]'), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('sy.yzz.cn/sycyz/cyxw/' + s5 + '-\d+\.shtml$'), restrict_xpaths='//ul[@class="allnews clearfix"]'), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # <div id="article"><script type="text/javascript" src="http://common.yzz.cn/home/address.js?pubdate=2016-10-21 19:18
        if len(sel.xpath('//div[@id="article" and contains(script/@src, "pubdate=' + s2 + '")]')) > 0:
            item = global_parse_content(response, '[@id="article"]')
            if item is not None:
                yield item
        
class sgamelookSpider(CrawlSpider):
    name = 'sgamelookSpider'
    allowed_domains = ['gamelook.com.cn']
    start_urls = [
        'http://www.gamelook.com.cn',
        'http://www.gamelook.com.cn/category/news',
        'http://www.gamelook.com.cn/category/news/page/2',
        'http://www.gamelook.com.cn/category/%E2%98%85%E6%89%8B%E6%9C%BA%E6%B8%B8%E6%88%8F',
        'http://www.gamelook.com.cn/category/%E2%98%85%E6%89%8B%E6%9C%BA%E6%B8%B8%E6%88%8F/page/2',
    ]
    rules = [
        #http://www.gamelook.com.cn/2016/10/267593 ok
        Rule(LinkExtractor(allow=('www.gamelook.com.cn/' + s9 + '/\d+$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        #<span class="meta-date">on 2016-10-10</span>
        if len(sel.xpath(u'//span[@class="meta-date" and contains(text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class sgameresSpider(CrawlSpider):
    name = 'sgameresSpider'
    allowed_domains = ['gameres.com']
    start_urls = [
        'http://www.gameres.com',
        'http://www.gameres.com/zuixin_1.html',
        'http://www.gameres.com/zuixin_2.html',
    ]
    rules = [
        #http://www.gameres.com/685813.html ok
        #div class="content"
        Rule(LinkExtractor(allow=('www.gameres.com/\d+\.html$'), restrict_xpaths='//div[@class="content"] | //a[@target="_blank"]'), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        #<p class="xg1">发布者:<span class="pipe">|</span>发布时间: 2016-10-13 10:43<span class="pipe">|</span>评论数: 1</p>
        if len(sel.xpath(u'//p[@class="xg1" and contains(string(.), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class syouxiputaoSpider(CrawlSpider):
    name = 'syouxiputaoSpider'
    allowed_domains = ['youxiputao.com']
    start_urls = [
        'http://youxiputao.com',
        'http://youxiputao.com/article',
        'http://youxiputao.com/article/index/page/2',
    ]
    rules = [
        #http://youxiputao.com/articles/10143 ok
        #<ul class="news-list"><li class="col-xs-12">
        Rule(LinkExtractor(allow=('youxiputao.com/articles/\d+$'), restrict_xpaths='//ul[@class="news-list"]'), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # <div class="time"><b>来自 游戏葡萄 2016-10-13 </b></div>
        if len(sel.xpath(u'//div[@class="time" and contains(b/text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class sgamedogSpider(CrawlSpider):
    name = 'sgamedogSpider'
    allowed_domains = ['gamedog.cn']
    start_urls = [
        'http://www.gamedog.cn',
        'http://news.gamedog.cn/',
        'http://online.gamedog.cn/',
        'http://www.gamedog.cn/games/',
        'http://www.gamedog.cn/news/',
        'http://news.gamedog.cn/a/yejiedongtai_242_1.html',
        'http://news.gamedog.cn/a/yejiedongtai_242_2.html',
        'http://news.gamedog.cn/a/yejiedongtai_242_3.html',
        'http://news.gamedog.cn/list_32252_1.html',
        'http://news.gamedog.cn/list_32252_2.html',
        'http://news.gamedog.cn/list_32252_3.html',
        'http://news.gamedog.cn/list_zonghe_1.html',
        'http://news.gamedog.cn/list_zonghe_2.html',
        'http://news.gamedog.cn/list_zonghe_3.html',
        'http://www.gamedog.cn/news/list_3442_1.html',
        'http://www.gamedog.cn/news/list_3442_2.html',
        'http://www.gamedog.cn/news/list_3442_3.html',
    ]
    rules = [
        #http://news.gamedog.cn/a/20160921/1885957.html ok
        #http://www.gamedog.cn/news/20161013/1907599.html ok
        Rule(LinkExtractor(allow=('news.gamedog.cn/a/' + s4 + '/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.gamedog.cn/news/' + s4 + '/\d+\.html$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        item = global_parse_content(response)
        if item is not None:
            yield item

class syxdownSpider(CrawlSpider):
    name = 'syxdownSpider'
    allowed_domains = ['yxdown.com']
    start_urls = [
        'http://www.yxdown.com',
        'http://www.yxdown.com/m/',
        'http://www.yxdown.com/ol/',
        'http://www.yxdown.com/news/',
        'http://www.yxdown.com/news/zixun/',
        'http://www.yxdown.com/news/wangluo/',
        'http://www.yxdown.com/news/shouyou/',
        'http://www.yxdown.com/mnews/',
        'http://www.yxdown.com/mnews/page2/',
        'http://www.yxdown.com/mnews/page3/',
        'http://www.yxdown.com/mnews/page4/',
        'http://www.yxdown.com/mnews/page5/',
        'http://www.yxdown.com/mnews/wangyou/',
        'http://www.yxdown.com/mnews/wangyou/page2/',
        'http://www.yxdown.com/mnews/wangyou/page3/',
        'http://www.yxdown.com/mnews/wangyou/page4/',
        'http://www.yxdown.com/mnews/wangyou/page5/',
        'http://www.yxdown.com/olnews/',
        'http://www.yxdown.com/olnews/zixun/',
        'http://www.yxdown.com/olnews/zixun/2/',
    ]
    rules = [
        #http://www.yxdown.com/news/201610/316523.html ok
        #http://www.yxdown.com/mnews/316031.html ok
        #http://www.yxdown.com/olnews/311282.html ok
        Rule(LinkExtractor(allow=('www.yxdown.com/news/' + s5 + '/\d+\.html$'), restrict_xpaths='//div[@class="new_zixun"]'), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.yxdown.com/olnews/\d+\.html$'), restrict_xpaths='//div[@id="newscon" or @id="soft-news" or @class="jd_m"]'), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.yxdown.com/mnews/\d+\.html$'), restrict_xpaths='//div[@class="contNews" or @class="hotcon"]'), callback='parse_content2', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        #news olnews <div id="nArticle_title"><p><b>2016年10月24日 来源：游迅网 编辑：稻草人  </b></p>
        if len(sel.xpath(u'//div[@id="nArticle_title" and contains(p/b/text(), "' + s12 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

    def parse_content2(self, response):
        sel = Selector(response)
        #mnews <div class="art"><p class="time">2016年10月20日 来源: 游迅网 编辑：  阿木木 [已有<span style="color:red">0</span>人评论]</p>
        if len(sel.xpath(u'//p[@class="time" and contains(text(), "' + s12 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class s07073Spider(CrawlSpider):
    name = 's07073Spider'
    allowed_domains = ['07073.com']
    start_urls = [
        'http://www.07073.com',
        'http://xin.07073.com/',
        'http://xin.07073.com/zixun/',
        'http://xin.07073.com/zixun/list_70_2.html',
        'http://chanye.07073.com/',
        'http://chanye.07073.com/hydt/',
        'http://chanye.07073.com/hydt/list_18536_2.html',
    ]
    rules = [
        #http://xin.07073.com/guonei/1467565.html ok
        #http://chanye.07073.com/shuju/1466199.html ok

        #xin <div class="xinBigList"><ul><li><span>2016-10-24</span><h4>
        #chanye <div class="new15IndexList" id="news">
        #chanye <div class="new15BigList"><ul><li><span>2016-10-24</span><a href="http://chanye.07073.com/guowai/1475342.html"

        Rule(LinkExtractor(allow=('xin.07073.com/[a-z]+/\d+\.html$'), restrict_xpaths='//div[@class="xinBigList"]'), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('chanye.07073.com/[a-z]+/\d+\.html$'), restrict_xpaths='//div[@class="new15IndexList" or @class="new15BigList"]'), callback='parse_content2', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        # xin <h4 class="epInfo">来源：<span>07073游戏网</span>&nbsp;&nbsp;&nbsp;&nbsp;作者：360uu&nbsp;&nbsp;&nbsp;&nbsp;发布时间：2016-10-13 10:01&nbsp;&nbsp;&nbsp;&nbsp;
        if len(sel.xpath('//h4[@class="epInfo" and contains(string(.), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

    def parse_content2(self, response):
        sel = Selector(response)
        # chanye <li class="tsax_1">2016-10-24 14:01</li>
        if len(sel.xpath('//li[@class="tsax_1" and contains(text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class s18183Spider(CrawlSpider):
    name = 's18183Spider'
    allowed_domains = ['18183.com']
    start_urls = [
        'http://www.18183.com',
        'http://news.18183.com/',
        'http://news.18183.com/list_218_2.html',
        'http://news.18183.com/list_218_3.html',
        'http://news.18183.com/list_218_4.html',
        'http://news.18183.com/list_218_5.html',
        'http://xin.18183.com/news/',
        'http://xin.18183.com/news/list_906_2.html',
        'http://chanye.18183.com/zxxw/'
        'http://chanye.18183.com/zxxw/list_1204_2.html',
        'http://chanye.18183.com/cytt/',
        'http://chanye.18183.com/cytt/list_1196_2.html',
        'http://iphone.18183.com/xinwen/',
        'http://iphone.18183.com/xinwen/list_88_2.html',
        'http://ipad.18183.com/xinwen/',
        'http://ipad.18183.com/xinwen/list_141_2.html',
    ]
    rules = [
        #http://news.18183.com/yxxw/201610/713622.html ok
        #http://xin.18183.com/201610/712248.html ok
        #http://chanye.18183.com/201610/713770.html ok
        #http://iphone.18183.com/xinwen/yxxw/201610/713969.html ok
        #http://android.18183.com/xinwen/yxxw/201610/714578.html ok
        #http://android.18183.com/xiazai/326576.html no
        #http://vr.18183.com/201610/713754.html no
        #http://danji.18183.com/201610/713807.html no
        #http://pada.18183.com/news/7530.html no
        Rule(LinkExtractor(allow=('news.18183.com/yxxw/' + s5 + '/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('chanye.18183.com/' + s5 + '/\d+\.html$')), callback='parse_content2', follow=True),
        Rule(LinkExtractor(allow=('xin.18183.com/' + s5 + '/\d+\.html$')), callback='parse_content3', follow=True),
        Rule(LinkExtractor(allow=('iphone.18183.com/xinwen/yxxw/' + s5 + '/\d+\.html$')), callback='parse_content3', follow=True),
        Rule(LinkExtractor(allow=('android.18183.com/xinwen/yxxw/' + s5 + '/\d+\.html$')), callback='parse_content3', follow=True),
        Rule(LinkExtractor(allow=('ipad.18183.com/xinwen/yxxw/' + s5 + '/\d+\.html')), callback='parse_content3', follow=True),
    ]
    
    def parse_content(self, response):
        sel = Selector(response)
        #news <div class="content_detail"><p class="other"><span>来源：www.18183.com</span><span>作者：纠结的乌龟</span><span>时间：2016-10-24</span>
        if len(sel.xpath('//p[contains(@class, "other") and contains(string(.), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

    def parse_content2(self, response):
        sel = Selector(response)
        #chanye <div class="txtlist"><h1>马化腾对话钱颖一：微信最初就是一个邮箱</h1><div class="a_info">来源：chanye.18183.com    作者：游民老赵      时间：16-10-24</div>
        if len(sel.xpath('//div[contains(@class, "a_info") and contains(text(), "' + s10 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

    def parse_content3(self, response):
        sel = Selector(response)
        #xin iphone ipad <p class="tit_bk_fx"><span>来源：www.18183.com</span><span>作者：南山顽石 </span><span>时间：2016-10-24</span></p>
        if len(sel.xpath('//p[contains(@class, "tit_bk_fx") and contains(string(.), "' + s10 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class syoyouSpider(CrawlSpider):
    name = 'syoyouSpider'
    allowed_domains = ['yoyou.net']
    start_urls = [
        'http://www.yoyou.net',
        'http://www.yoyou.net/zixun/',
        'http://www.yoyou.net/zixun/index_2.shtml',
        'http://www.yoyou.net/gldj/rmsy/',
        'http://www.yoyou.net/gldj/rmsy/index_2.shtml',
    ]
    rules = [
        #http://www.yoyou.net/wydt/120495.shtml ok
        #http://www.yoyou.net/zixun/dzjj/nizhan/141495.shtml
        Rule(LinkExtractor(allow=('www.yoyou.net/[a-z]+/\d+\.shtml$')), callback='parse_content', follow=True),
    ]

    #<p class="info"><span id="pubtime_baidu">2016-10-12 16:54:27</span>&nbsp;&nbsp;&nbsp;<span id="source_baidu">来源：<a href="/" target="_blank">网游动态</a></span></p>
    def parse_content(self, response):
        item = global_parse_content(response)
        if item is not None:
            yield item

class syouxituoluoSpider(CrawlSpider):
    name = 'syouxituoluoSpider'
    allowed_domains = ['youxituoluo.com']
    start_urls = [
        'http://www.youxituoluo.com',
        'http://www.youxituoluo.com/page/2',
        'http://www.youxituoluo.com/news',
        'http://www.youxituoluo.com/news/page/2',
        'http://www.youxituoluo.com/haiwai',
        'http://www.youxituoluo.com/haiwai/page/2',
        'http://www.youxituoluo.com/haiwai/rhsc',
        'http://www.youxituoluo.com/haiwai/rhsc/page/2',
        'http://www.youxituoluo.com/chanye',
        'http://www.youxituoluo.com/chanye/page/2',
    ]
    rules = [
        #http://www.youxituoluo.com/501789.html ok
        #<section id="news"><section><a target="_blank" class="left_img" href="/502049.html"><p class="subtitle"><time datetime="2016-10-24">2016-10-24</time>
        Rule(LinkExtractor(allow=('www.youxituoluo.com/\d+\.html$'), restrict_xpaths='//p[@class="subtitle" and contains(time/text(), "' + s2 + '")]/..'), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        #<p class="introduction"><time>2016-10-22</time>
        if len(sel.xpath('//p[@class="introduction" and contains(time/text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item
        
class sgcoresSpider(CrawlSpider):
    name = 'sgcoresSpider'
    allowed_domains = ['g-cores.com']
    start_urls = [
        'http://www.g-cores.com',
        'http://www.g-cores.com/categories/1/originals',
        'http://www.g-cores.com/categories/2/originals',
    ]
    rules = [
        #http://www.g-cores.com/articles/20960 ok
        #<div class="showcase_time"><span><a target="_self" href="http://www.g-cores.com/categories/27">玩出花儿来</a></span>2016-10-23</div>
        Rule(LinkExtractor(allow=('www.g-cores.com/articles/\d+$'), restrict_xpaths='//div[@class="showcase_time" and contains(string(.), "' + s2 + '")]/..'), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        #<p class="story_info">2016-10-13 15:56:41</p>
        if len(sel.xpath('//p[@class="story_info" and contains(text(), "' + s2 + '")]')) > 0:
            item = global_parse_content(response)
            if item is not None:
                yield item

class gameIpSpider(CrawlSpider):
    # name of spiders
    name = 'gameIpSpider'
    #allow_domain = ['17173.com']
    start_urls = [
        'http://www.17173.com',
        'http://www.duowan.com',
        'http://games.qq.com',
        'http://games.sina.com.cn',
        'http://www.uuu9.com',
        'http://www.pcgames.com.cn',
        'http://www.tgbus.com',
        'http://play.163.com',
        'http://www.178.com',
        'http://www.youxiduo.com',
        'http://www.gamersky.com',
        'http://www.ali213.net',
        'http://www.3dmgame.com',
        'http://www.yzz.cn',
        'http://www.gamelook.com.cn',
        'http://www.gameres.com',
        'http://youxiputao.com',
        'http://www.gamedog.cn',
        'http://www.yxdown.com',
        'http://www.07073.com',
        'http://www.18183.com',
        'http://www.yoyou.net',
        'http://www.youxituoluo.com',
        'http://www.g-cores.com',
        #'https://cowlevel.net', 需要注册
    ]
    rules = [
        #http://news.17173.com/content/10132016/160912434.shtml ok
        #http://newgame.17173.com/news/10112016/101540273_1.shtml ok
        Rule(LinkExtractor(allow=('news.17173.com/content/\d{4}201[6-9]/\w+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('newgame.17173.com/news/\d{4}201[6-9]/\w+\.shtml$')), callback='parse_content', follow=True),

        #http://www.duowan.com/1610/340301585593.html
        #http://news.duowan.com/1610/340279015237.html ok
        #http://newgame.duowan.com/1610/340055564665.html ok
        #http://ps4.duowan.com/1610/340304594896.html no
        #http://3ds.duowan.com/1610/340304594896.html no
        #http://psv.duowan.com/1610/340304594896.html no
        #http://vrgame.duowan.com/1610/340287388551.html no
        #http://www.5253.com/articles/316830.html ok
        Rule(LinkExtractor(allow=('www.duowan.com/1[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('news.duowan.com/1[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('newgame.duowan.com/1[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.5253.com/articles/\d+\.html$')), callback='parse_content', follow=True),

        #http://games.qq.com/a/20161013/019028.htm ok
        Rule(LinkExtractor(allow=('games.qq.com/a/[201][6-9]\d{4}/\d+\.htm$')), callback='parse_content', follow=True),

        #http://games.sina.com.cn/t/n/2016-10-13/fxwvpar7913096.shtml ok
        #http://games.sina.com.cn/ol/n/2016-10-13/fxwvpar7916088.shtml ok
        Rule(LinkExtractor(allow=('games.sina.com.cn/[A-Za-z]+/n/\[201][6-9]-\d{1,2}-\d{1,2}/\w+\.shtml$')), callback='parse_content', follow=True),

        #http://news.uuu9.com/china/201610/395727.shtml ok
        #http://news.uuu9.com/rihan/201608/392530.shtml ok
        #http://news.uuu9.com/oumei/201603/381718.shtml ok
        #http://www.yoyojie.com/syzx/20161013/234290.shtml ok
        #http://www.yoyojie.com/pingce/20161013/234271.shtml ok
        Rule(LinkExtractor(allow=('news.uuu9.com/[A-Za-z]+/201[6-9]\d{2}/\d+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.yoyojie.com/[A-Za-z]+/201[6-9]\d{4}/\d+\.shtml$')), callback='parse_content', follow=True),
        
        #http://news.pcgames.com.cn/638/6388759.html ok
        #http://ng.pcgames.com.cn/618/6180594.html ok
        #http://sy.pcgames.com.cn/641/6411033.html ok
        #http://pc.pcgames.com.cn/638/6382902.html no
        #http://wangyou.pcgames.com.cn/641/6410234.html no
        #http://web.pcgames.com.cn/641/6413032.html no
        #http://fight.pcgames.com.cn/641/6413012.html no
        Rule(LinkExtractor(allow=('news.pcgames.com.cn/\d+/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('ng.pcgames.com.cn/\d+/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('sy.pcgames.com.cn/\d+/\d+\.html$')), callback='parse_content', follow=True),
        
        #http://shouji.tgbus.com/201610/9840495168.html ok
        #http://ol.tgbus.com/201610/2477395997.html no 
        #http://ps4.tgbus.com/news/201610/20161013103730.shtml no
        #http://3ds.tgbus.com/news/newslist/201610/20161011134535.shtml no
        #http://xbox360.tgbus.com/zixun/yenei/201610/20161005144443.shtml no
        Rule(LinkExtractor(allow=('shouji.tgbus.com/201[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),

        #http://play.163.com/16/1013/12/C38PO79P00314OSE.html ok
        #http://play.163.com/16/1013/17/C39AN9DI00314J6L.html ok
        Rule(LinkExtractor(allow=('play.163.com/\d+/\d+/\d+/\[A-Za-z0-9]+\.html$')), callback='parse_content', follow=True),
        
        #http://news.178.com/201610/270237686264.html ok
        #http://xin.178.com/201610/270345146131.html ok
        #http://shouyou.178.com/201610/2433295991.html ok
        Rule(LinkExtractor(allow=('news.178.com/201[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('xin.178.com/201[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('shouyou.178.com/201[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        
        #http://www.youxiduo.com/content/tTHySVXECRwF.html ok
        Rule(LinkExtractor(allow=('www.youxiduo.com/content/.*\.html$')), callback='parse_content', follow=True),
        
        #http://www.gamersky.com/news/201610/818775.shtml ok
        #http://shouyou.gamersky.com/news/201610/820649.shtml ok
        #http://ol.gamersky.com/news/201610/820636.shtml no
        Rule(LinkExtractor(allow=('www.gamersky.com/news/201[6-9]\d{2}/\d+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('shouyou.gamersky.com/news/201[6-9]\d{2}/\d+\.shtml$')), callback='parse_content', follow=True),
        
        #http://www.ali213.net/news/html/2016-10/254523.html ok
        #http://m.ali213.net/news/161014/64229.html ok
        #http://web.ali213.net/news/html/2016-10/325783.html no
        Rule(LinkExtractor(allow=('www.ali213.net/news/html/201[6-9]-\d{1,2}/\d+\.shtml$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('m.ali213.net/news/1[6-9]\d{4}/\d+\.html$')), callback='parse_content', follow=True),
        
        #http://www.3dmgame.com/news/201610/3598748.html ok
        Rule(LinkExtractor(allow=('www.3dmgame.com/news/201[6-9]\d{2}/\d+\.shtml$')), callback='parse_content', follow=True),
        
        #http://news.yzz.cn/domestic/201610-1018524.shtml ok
        Rule(LinkExtractor(allow=('news.yzz.cn/\w+/201[6-9]-\d2-\d+\.shtml$')), callback='parse_content', follow=True),
        
        #http://www.gamelook.com.cn/2016/10/267593 ok
        Rule(LinkExtractor(allow=('www.gamelook.com.cn/201[6-9]/\d{1,2}/\d+$')), callback='parse_content', follow=True),
        
        #http://www.gameres.com/685813.html ok
        Rule(LinkExtractor(allow=('www.gameres.com/\d+\.html$')), callback='parse_content', follow=True),
        
        #http://youxiputao.com/articles/10143 ok
        Rule(LinkExtractor(allow=('youxiputao.com/articles/\d+$')), callback='parse_content', follow=True),

        #http://news.gamedog.cn/a/20160921/1885957.html ok
        #http://www.gamedog.cn/news/20161013/1907599.html ok
        Rule(LinkExtractor(allow=('news.gamedog.cn/a/201[6-9]\d{4}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.gamedog.cn/news/201[6-9]\d{4}/\d+\.html$')), callback='parse_content', follow=True),

        #http://www.yxdown.com/news/201610/316523.html ok
        #http://www.yxdown.com/mnews/316031.html ok
        #http://www.yxdown.com/olnews/311282.html no
        Rule(LinkExtractor(allow=('www.yxdown.com/news/201[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('www.yxdown.com/mnews/\d+\.html$')), callback='parse_content', follow=True),

        #http://xin.07073.com/guonei/1467565.html ok
        #http://chanye.07073.com/shuju/1466199.html ok
        Rule(LinkExtractor(allow=('xin.07073.com/[a-z]+/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('chanye.07073.com/[a-z]+/\d+\.html$')), callback='parse_content', follow=True),

        #http://news.18183.com/yxxw/201610/713622.html ok
        #http://xin.18183.com/201610/712248.html ok
        #http://chanye.18183.com/201610/713770.html ok
        #http://pada.18183.com/news/7530.html ok
        #http://iphone.18183.com/xinwen/yxxw/201610/713969.html ok
        #http://android.18183.com/xinwen/yxxw/201610/714578.html ok
        #http://android.18183.com/xiazai/326576.html ok
        #http://vr.18183.com/201610/713754.html no
        #http://danji.18183.com/201610/713807.html no
        Rule(LinkExtractor(allow=('news.18183.com/yxxw/201[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('xin.18183.com/201[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('chanye.18183.com/201[6-9]\d{2}/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('pada.18183.com/news/\d+\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('android.18183.com/.*\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('iphone.18183.com/.*\.html$')), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=('ipad.18183.com/.*\.html$')), callback='parse_content', follow=True),

        #http://www.yoyou.net/wydt/120495.shtml ok
        Rule(LinkExtractor(allow=('www.yoyou.net/[a-z]+/\d+\.html$')), callback='parse_content', follow=True),

        #http://www.youxituoluo.com/501789.html ok
        Rule(LinkExtractor(allow=('www.youxituoluo.com/\d+\.html$')), callback='parse_content', follow=True),

        #http://www.g-cores.com/articles/20960 ok
        Rule(LinkExtractor(allow=('www.g-cores.com/articles/\d+\.html$')), callback='parse_content', follow=True),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        title = sel.xpath('//title/text()').extract_first()
        content = sel.xpath(u'//div//p[( \
            contains(text(), "妖尾") or\
            contains(text(), "妖精的尾巴") or\
            contains(text(), "妖精尾巴") or \
            contains(text(), "魔导少年")) \
            and (\
            contains(text(), "IP") or\
            contains(text(), "手游") or\
            contains(text(), "改编") or\
            contains(text(), "授权") or\
            contains(text(), "中国") or\
            contains(text(), "大陆")\
            )]//text()').extract()
        
        if len(content) > 0:
            item = GameInfoItem()
            item['url'] = response.url
            item['title'] = title
            item['content'] = content[0]
            yield item
