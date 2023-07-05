import time
#import financialNews.core.finance.cnfol, financialNews.core.eastmoney, financialNews.core.sina, snowball
from financialNews.core.finance import cnfol
from financialNews.core.finance import eastmoney
from financialNews.core.finance import sina
from financialNews.core.finance import snowball

from financialNews.utils import util

def fetch(*args):
    if args[0] == 'Ashare':
        ret = eastmoney.collect_ashare(args[1])
    elif args[0] == 'gold':
        ret = cnfol.collect_gold()
    elif args[0] == 'btc':
        ret = sina.collect_btc()
    elif args[0] == 'rmb':
        ret = sina.collect_rmb()
    elif args[0] == 'inx':
        ret = snowball.collect_inx()
    else:
        raise Exception("finance fetch arg error")
    return ret

def fetch_all(target_config, size):
    new_size = size
    all = []
    for target in target_config:
        data = fetch(*target[1:])
        if len(data) < new_size:
            new_size = len(data)
        all.append(data)
        # 降低请求频率
        time.sleep(5)
    if size <= 0:
        raise Exception("size <= 0")
    if len(all) != len(target_config):
        raise Exception("finance fetch all data lost")
    short_data = []
    # 每种数据截取相同数量
    for node in all:
        new_node = util.list2d_to_DataFrame(node[-new_size:], 'open_high_low_close')
        short_data.append(new_node)
    return short_data
