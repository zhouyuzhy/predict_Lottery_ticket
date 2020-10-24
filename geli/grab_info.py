from bs4 import BeautifulSoup
import requests
import pandas as pd

if __name__ == '__main__':
    url = 'https://mall.gree.com/goods/search/searchItem'
    products = []
    for page in [1, 2, 3]:
        d = {'page': page, 'brandId': '', 'attrId': '',
             # 'attributes': '14:631850;15:631856;',
             'attributes': '14:631816;',
             'keyword': '',
             'orderSort': 0, 'payType': '',
             # 'cid': [853, 1000286729, 1000042693, 1000055000, 1000287442, 1000052342, 1000269141, 1000289772,
             #         1000287445, 1000052340, 1000285942, 1000269142, 1000290025, 1000290980, 1000289192, 1000050312,
             #         1000289287, 1000290988, 1000297596, 1000297598, 1000297793, 1000297814, 1000293212, 1000297968,
             #         1000297884, 1000297442, 1000290986, 1000290982, 1000297969]
             'cid': [852, 1000298583, 1000259942, 1000259941, 1000259940, 1000296222, 1000294747, 1000294746,
                     1000286752, 1000286751, 1000293595, 1000293594, 1000285933, 1000293125, 1000293127, 1000293123,
                     1000293126, 1000293124, 1000292724, 1000292515, 1000292514, 1000292512, 1000292511, 1000292513,
                     1000292510, 1000292509, 1000279127, 1000290992, 1000279114]
             }
        r = requests.post(url, data=d)
        soup = BeautifulSoup(r.text)
        div_search_list = soup.find_all("div", class_='Product_box')
        for product in div_search_list:
            p = {}
            products.append(p)
            a_href = product.find_all('p', class_='fl')[0].find_all('a')[0]
            title = a_href.attrs['title'][0:a_href.attrs['title'].index('变频')]
            detail_page_url = 'https://mall.gree.com' + a_href.attrs['href']
            price = product.find_all('div', class_='jiaqian')[0].find_all('strong')[0]
            price = price.text.replace('￥', '')
            p['title'] = title
            p['url'] = detail_page_url
            p['price'] = price
            detail_page = requests.get(detail_page_url)
            detail_page_soup = BeautifulSoup(detail_page.text)
            c_keys = detail_page_soup.find_all('div', class_='TabContent')[0].find_all('label', class_='cKey')
            for c_key in c_keys:
                k = c_key.text
                v = c_key.next_element.next_element.replace('\r\n', '').replace(' ', '')
                p[k] = v
    print(products)
    products_df = pd.DataFrame(products)
    products_df.to_csv('products_guaji.csv')
