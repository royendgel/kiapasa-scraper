from scrapy import Spider, Request
from scraper.items import Ad


class ViaViaSpider(Spider):
    name, start_urls = 'viavia', [
        'http://www.curacaoexchange.com/',
    ]

class MarktPlaatsSpider(Spider):
    name, start_urls = 'marktplaats', [
        'http://marktplaats.cw',

        ]

    """
    Get all categories, and prcess_all
    """

    def parse(self, response):
        n = 0
        for url in response.css('li'):
            u = url.css('a::attr(href)').extract()[0]
            self.cur_url = self.start_urls[0] + u
            if u.startswith('/ads'):
                yield Request(self.cur_url, self.get_pages)
                # yield Request(self.start_urls[0] + u, self.parse_ads)

        # return [Ad(title = r.extract()) for r in response.css('.title.breakall')]

    def parse_ads(self, response):
        for item in response.css('.item'):
            yield Request(self.start_urls[0] + item.css('a::attr(href)').extract()[0], self.parse_detail)

    def get_pages(self, response):
        """
        I will take the number based on the last number shown.

        """
        for page in response.css('div.pages'):
            try:
                n = int(page.css('a::text').extract()[-1])
                for p in xrange(1, n+1):
                    url =  "%s/page/%s" %(response._url,p)
                    yield Request(url, self.parse_ads)

            except:
                print 'not converted to int'

    def parse_detail(self, response):
        title = response.css('.title.breakall::text').extract()[0]
        price = response.css('.price::text').extract()[0]
        text = response.css('div.text::text').extract()[0]
        ad = Ad(title=title, price=price,text=text)
        return ad