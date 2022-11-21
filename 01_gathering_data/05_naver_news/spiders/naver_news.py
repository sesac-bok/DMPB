import scrapy
import datetime
import re
from bok.items import NaverNews
from ..middlewares import TooManyRequestsRetryMiddleware
import time
import pandas as pd
import logging


class NaverNewsSpider(scrapy.Spider):
    name = 'naver_news'
    start_urls = ['http://search.naver.com/']
    crawled_url = []
    custom_settings = {
        'DOWNLOADER_CLIENTCONTEXTFACTORY': 'bok.contextfactory.LegacyConnectContextFactory',
    }

    def start_requests(self):
        start_date = '20080401'
        end_date = '20221115'
        search_day = '20080401'
        self.retry_url = []
        url_list = []
        while True:
            if int(search_day) <= int(end_date):
                # 1001 : 연합뉴스
                # 1018 : 이데일리
                # 2227 : 연합인포맥스
                for news_company in ['1001', '1018', '2227']:
                    url = 'https://search.naver.com/search.naver?&where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=3&ds={0}&de={1}&news_office_checked={2}&docid=&nso=so:dd,p:,a:all&mynews=1&start=1&refresh_start=0'.format(
                        search_day, search_day, news_company)
                    # print(url, search_day)
                    url_list.append([url, search_day])
            else:
                break
            search_day = pd.to_datetime(search_day) + datetime.timedelta(days=1)
            search_day = search_day.strftime('%Y%m%d')
        for urls, se_date in url_list:
            yield scrapy.Request(url=urls,
                                 meta={'date': se_date},
                                 callback=self.parse_news)

    def parse_news(self, response):
        # self.logger.critical(response.url)
        if response.url not in self.crawled_url:
            self.crawled_url.append(response.url)
            articles = response.xpath('//*[@id="main_pack"]/section/div/div[2]/ul/li')

            for article in articles:
                media = article.xpath('./div/div/div[1]/div[2]/a[1]/text()').get().strip()
                page_url = article.xpath('./div/div/a/@href').get()
                cur_date = response.meta['date']
                page_url_fake_user = page_url
                yield scrapy.Request(
                    page_url_fake_user,
                    callback=self.parse_page,
                    meta={"media": media, "date": cur_date, 'url': page_url},
                )
        next_page = response.xpath('//*[@id="main_pack"]/div[2]/div/a[2]/@href')
        if next_page != []:
            yield response.follow(
                next_page[-1].get(),
                meta={'date': cur_date},
                callback=self.parse_news)

    def parse_page(self, response):
        logging.info("response.status:%s" % response.status)
        logourl = response.selector.css('div.main-nav__logo img').xpath('@src').extract()
        logging.info('response.logourl:%s' % logourl)
        item = NaverNews()
        item["media"] = response.meta["media"]
        item["date"] = response.meta["date"]
        item["url"] = response.meta["url"]
        if item["media"] == "연합인포맥스":
            time.sleep(0.2)
            title = response.xpath('//*[@id="user-container"]/div[3]/header/div/div/text()').get()
            content = response.xpath('//*[@id="article-view-content-div"]/text()').getall()
        elif item["media"] == "이데일리":
            title = response.xpath('//*[@id="contents"]/section[1]/section[1]/div[1]/div[1]/h2/text()').get()
            content = response.xpath(
                '//*[@id="contents"]/section[1]/section[1]/div[1]/div[3]/div[1]/text()').getall()
        else:
            # 연합뉴스
            if 'naver' in response.url:
                title = response.xpath('//*[@id="ct"]/div[1]/div[2]/h2/text()').get()
                content = response.xpath('//*[@id="dic_area"]/text()').getall()
            else:
                title = response.xpath('//*[@id="articleWrap"]/div[1]/header/h1/text()').get()
                content = response.xpath('//*[@id="articleWrap"]/div[2]/div/div/article/p/text()').getall()

        re_content = ' '.join([re.sub('[^a-z가-힣ㄱ-ㅎ0-9., ]', '', cnt).strip() for cnt in content]).strip()
        if content != [] and re_content != '':
            if title:
                re_title = re.sub('[^a-z가-힣ㄱ-ㅎ0-9., ]', '', title).strip()
            else:
                title = ''
            item['content'] = re_title + re_content
            yield item
        else:
            print('retry', response.meta["url"])
            with open('retry_url_080401~151115.csv', 'a', encoding='utf-8') as f:
                f.write(','.join([response.url]) + ',' + response.meta["date"])
                f.write('\n')
