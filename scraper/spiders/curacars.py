from scrapy import Spider, Request
from scraper.items import Ad


class ViaViaSpider(Spider):
    name, start_urls = 'viavia', [
        'http://www.curacaoexchange.com/',

        ]

    """
    Get all categories, and prcess_all
    """

    def parse(self, response):
        print response