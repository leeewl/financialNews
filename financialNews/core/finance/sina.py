import re

import requests
from financialNews.utils import util

def collect_btc():
    url = "https://quotes.sina.cn/fx/api/openapi.php/BtcService.getDayKLine?symbol=btcbtcusd"
    response_json = util.get_url(url)
    data = response_json['result']['data']
    data_list = data.split('|')
    all_data = []
    for node in data_list:
        l = node.split(',')
        all_data.append(l[0:6])
    return all_data

def collect_rmb():
    url = "https://vip.stock.finance.sina.com.cn/forex/api/jsonp.php/var%20_fx_susdcnh2023_6_29=/NewForexService.getDayKLine?symbol=fx_susdcnh&_=2023_6_29"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(response.content)
    result = re.findall(r'["](.*?)["]', response.text)
    if result == []:
        raise Exception("collect data of rmb,no result")
    data = result[0]
    data_rmb = data.split('|')
    all_data = []
    for node in data_rmb:
        arr = node.split(',')
        all_data.append(arr[0:5])
    return all_data

if __name__ == "__main__":
    ret = collect_rmb()
    print(ret)
