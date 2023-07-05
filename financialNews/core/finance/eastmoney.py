from financialNews.utils import util

def ashare_params(code):
    """东方财富请求参数"""
    tmp = "1." + code
    prms = {
        "secid": tmp,
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        # "klt": "102",
        "klt": "101",
        'fqt': "1",
        "end": "20500101",
        'lmt': "120",
    }
    result = ""
    for key, val in prms.items():
        result = result + key + "=" + val + "&"
    result = result[:-1]
    return result

def collect_ashare(code):
    server = "http://3.push2his.eastmoney.com/api/qt/stock/kline/get"
    params = ashare_params(code)
    url = server + "?" + params
    response = util.get_url(url)
    kline_data = response["data"]["klines"]

    all_data = []
    for node in kline_data:
        arr = node.split(",")
        #all_data.append(arr[0:6])
        all_data.append([arr[0], arr[1], arr[3], arr[4], arr[2]])
    return all_data

if __name__ == "__main__":
    code = "000016"
    ret = collect_ashare(code)
    print(ret)