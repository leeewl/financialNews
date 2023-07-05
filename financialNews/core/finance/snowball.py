from financialNews.config import config
from financialNews.utils import util

def get(url):
    Headers = {'Host': 'stock.xueqiu.com',
               'Accept': 'application/json',
               'Cookie': config.snowball_cookie,
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}

    response_json = util.get_url(url, Headers)
    items = response_json['data']['item']

    all_data = []
    for item in items:
        i = item[0:6]
        del i[1]
        all_data.append(i)
    return all_data

def collect_inx():
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=.INX&begin=1688133135492&period=day&type=before&count=-284&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"
    ret = get(url)
    return ret

if __name__ == "__main__":
    inx_info = collect_inx()
    print(inx_info)
