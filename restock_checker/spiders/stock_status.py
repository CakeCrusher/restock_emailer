import scrapy
from urllib.parse import urlencode
import datetime as dt
from send_email import sendEmail 
    
# add any site to check inventory status and fill in an object like so
# <string> : {'url': <string>, 'xpath': <string>, 'unavailable_text': <string>', 'render_js': <bool>}
sites_data = {
    'amazon_digital': {'url': 'https://www.amazon.com/dp/B08FC6MR62', 'xpath': '//*[@id="availability_feature_div"]/div/span/text()', 'unavailable_text': 'Currently unavailable', 'render_js': False},
    'amazon_controller': {'url': 'https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/dp/B08FC6C75Y', 'xpath': '//*[@id="availability_feature_div"]/div/span/text()', 'unavailable_text': 'Currently unavailable', 'render_js': False},
    # 'wallmart_digital': {'url': 'https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815', 'xpath': '//*[@id="blitzitem-container"]/div/div/div/div/b/text()', 'unavailable_text': 'out of stock', 'render_js': False},
    # 'target_digital': {'url': 'https://www.target.com/p/-/A-81114596', 'xpath': '//*[@id="viewport"]/div[4]/div/div[2]/div[3]/div[1]/div/div/div/text()', 'unavailable_text': 'Sold out', 'render_js': True},
    # 'bestbuy_digital': {'url': 'https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161', 'xpath': '//*[@class="fulfillment-add-to-cart-button"]/div/div/button/text()', 'unavailable_text': 'Sold Out', 'render_js': False},
    # 'wallmart_disc': {'url': 'https://www.walmart.com/ip/PlayStation-5-Console/363472942', 'xpath': '//*[@id="blitzitem-container"]/div/div/div/div/b/text()', 'unavailable_text': 'out of stock', 'render_js': False},
    # 'target_disc': {'url': 'https://www.target.com/p/playstation-5-console/-/A-81114595', 'xpath': '//*[@id="viewport"]/div[4]/div/div[2]/div[3]/div[1]/div/div/div/text()', 'unavailable_text': 'Sold out', 'render_js': True},
    # 'bestbuy_disc': {'url': 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149', 'xpath': '//*[@class="fulfillment-add-to-cart-button"]/div/div/button/text()', 'unavailable_text': 'Sold Out', 'render_js': False},
    }

# enter your https://www.scraperapi.com/ API Key
API_KEY = ''

def get_url(obj):
    # uses https://www.scraperapi.com/ proxy 
    sapi_payload = {'api_key': API_KEY, 'url': obj['url'], 'country_code': 'us', 'render': str(obj['render_js']).lower()}
    sapi_proxy_url = 'http://api.scraperapi.com/?' + urlencode(sapi_payload)
    return sapi_proxy_url

    # # without proxy (WARNING: uses your ip address)
    # return obj['url']

class StockStatusSpider(scrapy.Spider):
    name = 'stock_status'

    # makes the request to the provided website
    def start_requests(self):
        for name, att in sites_data.items():
            print(f'Starting: {name}')
            sites_data[name]['start_dt'] = dt.datetime.now()
            yield scrapy.Request(get_url(sites_data[name]), callback=self.parse_stock_status, meta={'name': name})
    
    # determined weather item is in stock and returns the following details:
    # {'name': <string>, 'availability': <bool>, 'availability_text': <string>, 'duration': <float>, 'start_dt': <datetime>}
    def parse_stock_status(self, response):
        item_obj = sites_data[response.meta['name']]
        availability_text = response.xpath(item_obj['xpath']).extract_first()
        if availability_text and item_obj['unavailable_text'] in availability_text:
            availability = False
        else:
            sendEmail(response.meta['name'], item_obj['url'])
            availability = True
        finish_time = dt.datetime.now()
        sites_data[response.meta['name']]['duration_seconds'] = (finish_time - sites_data[response.meta['name']]['start_dt']).total_seconds()
        yield {'name': response.meta['name'], 'availability': availability, 'availability_text': availability_text, 'duration': sites_data[response.meta['name']]['duration_seconds'], 'start_dt': sites_data[response.meta['name']]['start_dt']}
