import os
import scrapy
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy import Request

class YelpSpider(scrapy.Spider):

    name = 'yelp-spider'
    custom_settings = {"FEEDS": {"Test.csv": {"format": "csv"}},'CONCURRENT_REQUESTS': 1}
    headers = {
        'user-agent' :
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }

    try:
        os.remove('Test.csv')
    except OSError:  
        pass

    def start_requests(self):
            meta = {"proxy": "http://scraperapi.keep_headers=true:42c127e5bcae756cab41f1e3e099b8b1@proxy-server.scraperapi.com:8001"}
            i = 0
            print("iiiiiiiiiiiiiiii", i)
            url = f'https://www.yelp.com/search?find_desc=poke+bowl&find_loc=Conshohocken%2C+PA%2C+United+States&start={i}'
            yield scrapy.Request(url=url, meta=meta, headers=self.headers, callback=self.parse)

    def parse(self, response):
        details_link = response.xpath(".//span[@class=' css-1egxyvc'][@data-font-weight='bold']//a/@href").getall()
        print("ARQAM*****************", len(details_link))
        
        print("ARQAM*****************", details_link)

        
        # logo_url = response.xpath(".//img[@class=' css-xlzvdl']/@src").getall()
        # print("Logo*****************", len(logo_url))
        for details_link in details_link:
            absolute_url = response.urljoin(details_link)
            yield Request(absolute_url, callback=self.fetch_detail, meta={'absolute_url':absolute_url})

    def fetch_detail(self, response):
        print("Waheed*****************")
        link = response.meta.get('absolute_url')
        # print("link******************", link)
        logo_url = response.xpath('.//a[@class="photo-header-media-link__09f24__xmWtR css-1sie4w0"]//img/@src').get()
        # print("link******************", logo_url)
        lcompanyname = response.xpath(".//*[@class='css-12dgwvn']/text()").get()
        # print("link******************", lcompanyname)
        owner = response.xpath(".//section[@aria-label='About the Business']//p[@data-font-weight='bold']/text()").get()
        # print("link******************", owner)
        rating = response.xpath(".//div[contains(@aria-label, 'star')]/@aria-label").get()
        # print("link******************", rating)
        reviews = response.xpath(".//span[contains(text(),'reviews')]/text()").get()
        # print("link******************", reviews)
        delivery = response.xpath(".//span[contains(text(),'Offers Delivery')]/text()").get()
        # print("link******************", delivery)
        co_website = response.xpath(".//a[contains(text(),'http')]/text()").get()
        # print("link******************", co_website)
        co_tel = response.xpath(".//p[@class=' css-1p9ibgf'][contains(text(),'(')]/text()").get()
        # print("link******************", co_tel)

        yield{
        'Poke_Bowl_Shop_Name' : lcompanyname,
        'Owner': owner,
        "Rating": rating,
        "Reviews": reviews,
        'co_website': co_website, 
        "Delivery": delivery,
        "Tel_#": co_tel,
        "Link": link,
        'logo_url' : logo_url
        }


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(YelpSpider)
    process.start()