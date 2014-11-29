from scrapy import Spider, Request
from scraper.items import Ad

class ViaViaSpider(Spider):
    name, start_urls = 'viavia', [
        'http://www.curacaoexchange.com',

        ]

    """
    Get all categories, and prcess_all
    """

    def parse(self, response):
        for category in response.css('.adbox3'):
            try:
                cat =  category.css('h3 a::text').extract()[-1]
                link =  category.css('h3 a::attr(href)').extract()[-1]
                url = "%s%s" %(self.start_urls[0], link)
                yield Request(url, self.get_page)
                yield Request(url, self.get_all_pages)

            except:
                pass
        return

    def get_all_pages(self, response):
        """
        Get the first Page.
        Check if the page has numbers , or even has ads in it do something based on that answers.
        """
        active = True
        pages = []
        while active:
            if response.css('.pagination li a::text').extract()[-2] == "Next":
                pages.append(self.start_urls[0] + response.css('.pagination li a::attr(href)').extract()[-2])
            else:
                print 'active is false'
                active = False

        for page in pages:
            print 'Getting Page'
            yield Request(self.start_urls[0] + page, self.get_page)

    def get_page(self, response):
        print 'wwwww'
        for ad in response.css('.listtitle'):
            ad_link = ad.css('a::attr(href)').extract()
            if ad_link:
                yield Request(self.start_urls[0] + ad_link[0], self.extract_ad)

    def extract_ad(self, response):
        price, title, text = None, None, None
        title =  response.css('.detail-title::text').extract()[0]

        for thing in response.css('#main table tr'):
            for td in thing.css('td').extract():
                if 'Description' in td:
                    data = thing.css('td p').extract()
                    text = ''.join(data)

                elif 'Price' in td:
                    price = thing.css('td::text').extract()[1]
        link = response._url
        ad = Ad(title=title, price=price, text=text, link=link)
        return ad