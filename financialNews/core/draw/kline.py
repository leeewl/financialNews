import matplotlib.pyplot as plt
import mplfinance
import pandas as pd
import pandas.core.indexes.datetimes

from financialNews.utils import util
from financialNews.config import config

font = 'WenQuanYi Zen Hei'
# 解决中文乱码
#plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.sans-serif'] = [font]
plt.rcParams['axes.unicode_minus'] = False

def generate_picture(df, name, volume=True):
    if type(df.index) != pandas.core.indexes.datetimes.DatetimeIndex:
        if volume:
            data = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        else:
            data = df[['Date', 'Open', 'High', 'Low', 'Close']]
        data['Date'] = pd.to_datetime(data['Date'])
        # inplase代表在原数据上修改
        data.set_index("Date", inplace=True)
    else:
        if volume:
            data = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        else:
            data = df[['Open', 'High', 'Low', 'Close']]
    # 配色
    my_color = mplfinance.make_marketcolors(up='red',
                                            down='green',
                                            edge='black',
                                            wick='black',
                                            volume='cyan')
    # 风格
    my_style = mplfinance.make_mpf_style(marketcolors=my_color,
                                         gridaxis='both',
                                         gridstyle='-.',
                                         y_on_right=True,
                                         # 中文字体乱码
                                         rc={'font.family': font})
    print(f"plot {name} begin")
    # 画图
    mplfinance.plot(data.iloc[:, :],
                    type='candle',
                    style=my_style,
                    # 均线
                    mav=(5, 10, 20),
                    # 成交量
                    volume=volume,
                    # 标题
                    title=name,
                    # 保存
                    savefig=config.dir_picture + util.get_date_str() + name + '.png')
                    #savefig=util.get_date_str() + name + '.png')

def generate_all_picture(target_config, target_data):
    i = 0
    for target in target_config:
        generate_picture(target_data[i], target[0], False)
        print(f"generate .........{i}.....end")
        i += 1





