from financialNews.utils import util

def collect_gold():
    url = "http://gold.cnfol.com/fol_inc/v6.0/Gold/goldhq/json/g/autd/KlDay.json"
    ret = util.post_url(url)
    return ret

if __name__ == "__main__":
    ret = collect_gold()
    print(ret)
