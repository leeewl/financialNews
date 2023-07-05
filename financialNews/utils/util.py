import requests
import json
import pandas
import time
import datetime

def get_url(url, headers={}):
    if headers == {}:
        response = requests.get(url)
    else:
        response = requests.get(url, headers = headers)
    if response.status_code != 200:
        raise Exception(response.content)
    return json.loads(response.content)


def post_url(url, headers={}):
    if headers == {}:
        response = requests.post(url)
    else:
        response = requests.post(url, headers = headers)
    if response.status_code != 200:
        raise Exception(response.content)
    return json.loads(response.content)

def str_time_to_timestamp(str_time):
    #time_array = time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
    time_array = time.strptime(str_time, '%Y-%m-%d')
    print(time_array)
    timestamp = int(time.mktime(time_array))
    print(timestamp)
    return timestamp

def get_date_str():
    return datetime.date.today().strftime('%Y%m%d_')

# 二维列表转dataframe
def list2d_to_DataFrame(list2d, order):
    #list2d = [[1637856000000, 380.38, 383.5, 367.05, 371.2], [1638460800000, 369.7, 373.1, 363.2, 364.94], [1639065600000, 366.7, 367.7, 363.8, 364.55], [1639670400000, 366.8, 372, 363.1, 371.87], [1640275200000, 371.09, 373.46, 367.7, 371.55], [1640880000000, 371.35, 374.5, 368.17, 373.35], [1641484800000, 370.95, 375.15, 367.8, 368.2], [1642089600000, 368.5, 374.9, 367.01, 374.15], [1642694400000, 372.08, 377, 370.2, 376.45], [1645113600000, 382.8, 386.98, 376.73, 384.88], [1645718400000, 386.41, 400.09, 384.5, 389.55], [1646323200000, 390, 396, 383.39, 393.8], [1646928000000, 402.77, 419.26, 394.18, 403.35], [1647532800000, 402.62, 405.36, 387.75, 395], [1648137600000, 393.2, 402.53, 392, 400.18], [1648742400000, 401.44, 401.9, 387.75, 395], [1649347200000, 392.66, 398.94, 392.58, 397.9], [1649952000000, 398.1, 404.8, 395.11, 404.18], [1650556800000, 406.79, 407.55, 398.45, 404.5], [1651161600000, 402.8, 406.46, 397, 404.9], [1651766400000, 403.44, 405.8, 400.5, 404.95], [1652371200000, 404.8, 405.54, 394.3, 395.55], [1652976000000, 396.2, 399, 392.75, 396.84], [1653580800000, 397.83, 402.68, 394.93, 400.2], [1654185600000, 399.41, 401.75, 394.21, 397.95], [1654790400000, 396.51, 400.98, 394.5, 400.65], [1655395200000, 404.8, 404.88, 393, 397.95], [1656000000000, 397.01, 399, 392, 393.53], [1656604800000, 394.11, 396.3, 385.89, 389.65], [1657209600000, 389.9, 391, 373.18, 376.55], [1657814400000, 376.2, 379.48, 370.5, 372.12], [1658419200000, 371.7, 378.4, 368, 377], [1659024000000, 375.12, 385.1, 374.25, 384.7], [1659628800000, 383.5, 390.5, 382, 387.25], [1660233600000, 386.86, 392.6, 385.5, 390.96], [1660838400000, 391.83, 391.99, 385.01, 386.36], [1661443200000, 385.99, 390.76, 384.2, 387.95], [1662048000000, 388.13, 390.4, 381.07, 385.15], [1662652800000, 384.56, 390.15, 383.67, 389.76], [1663257600000, 388.88, 390.55, 383, 385.05], [1663862400000, 384.99, 387.88, 383.48, 385.15], [1664467200000, 383.83, 389.89, 382.61, 389.5], [1665676800000, 394.36, 396.7, 386.5, 390.2], [1666281600000, 390, 392.2, 387.52, 389.9], [1666886400000, 392.1, 394.7, 388.1, 391.31], [1667491200000, 391.44, 394, 389.36, 392.53], [1668096000000, 394.3, 438.87, 390, 406.67], [1668700800000, 407.17, 438.87, 402.25, 404.8], [1669305600000, 404.58, 407.5, 402.5, 406.8], [1669910400000, 408.77, 409.6, 402.33, 407.2], [1670515200000, 407.5, 409.49, 400.63, 404.5], [1671120000000, 405.67, 409, 401.33, 404.46], [1671724800000, 404.4, 410.88, 402.42, 407.8], [1672329600000, 407.38, 411.5, 405.82, 410], [1672934400000, 411.21, 414.69, 408.08, 412.69], [1673539200000, 413.41, 415.3, 408.71, 414.84], [1674144000000, 417.3, 423.42, 414.12, 422.3], [1675353600000, 420.9, 426.6, 413.31, 413.45], [1675958400000, 414.26, 418.75, 410, 411.77], [1676563200000, 412.24, 414.1, 410.32, 411.95], [1677168000000, 412.65, 414.8, 410.7, 412.99], [1677772800000, 413.23, 417.2, 412, 417.1], [1678377600000, 417.99, 420.28, 414.33, 419.72], [1678982400000, 422.6, 439.24, 416.69, 438.1], [1679587200000, 439.75, 448, 431.98, 441], [1680192000000, 438.7, 443.55, 433.35, 438.91], [1680796800000, 436.56, 447.15, 434.02, 445.43], [1681401600000, 443, 451.66, 440.26, 447], [1682006400000, 442.95, 449.58, 439.06, 439.8], [1682352000000, 440.8, 445.4, 439.2, 445.2]]

    list_date = []
    list_open = []
    list_high = []
    list_low = []
    list_close = []
    list_volume = []

    for list in list2d:
        if type(list[0]) == str:
            list[0] = str_time_to_timestamp(list[0])
        list_date.append(list[0])
        if order == 'open_high_low_close':
            list_open.append(float(list[1]))
            list_high.append(float(list[2]))
            list_low.append(float(list[3]))
            list_close.append(float(list[4]))
        else:
            list_open.append(float(list[1]))
            list_close.append(float(list[2]))
            list_high.append(float(list[3]))
            list_low.append(float(list[4]))

        if len(list) > 5:
            list_volume.append(float(list[5]))
    #
    list_dict = {
            'Date':list_date,
            'Open':list_open,
            'High':list_high,
            'Low':list_low,
            'Close':list_close
        }
    if list_volume:
        list_dict['Volume'] = list_volume

    #df_index = timestamplist_to_datetimeindex(list_date)
    df = pandas.DataFrame(
        list_dict,
    #    index=df_index
    )
    if len(str(list_date[0])) == 10:
        # 这有时区问题
        df['Date'] = pandas.to_datetime(df['Date'], origin='1970-01-01 08:00:00',unit="s")
    else:
        # 13位时间戳
        df['Date'] = pandas.to_datetime(df['Date'], origin='1970-01-01 08:00:00', unit="ms")

    return df

def same_day_as_today(timestamp):
    time_date = datetime.datetime.fromtimestamp(timestamp).date()
    now = datetime.datetime.now().timestamp()
    today_date = datetime.datetime.fromtimestamp(now).date()
    if time_date == today_date:
        return True
    else:
        return False
