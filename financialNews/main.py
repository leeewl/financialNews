import sys
import os
sys.path.append("/home/leeewl/code/financialNews")
# 上一级目录
sys.path.append(os.path.dirname(os.getcwd()))
# 虚拟环境包
sys.path.append(os.path.dirname(os.getcwd()) + "/venv/lib/python3.11/site-packages")

from core.finance import finance
from core.draw import kline
from core.wechat import wechat
from config import config

target_config = [
    ["上证50", "Ashare", "000016"],
    ["上证300", "Ashare", "000300"],
    ["中证500", "Ashare", "000905"],
    ["中证1000", "Ashare", "000852"],
    ["黄金日K","gold"],
    ["冰糖橙日K", "btc"],
    ["人民币汇率", "rmb"],
    ["标普500", "inx"]]


def upload_article(title='', author='', digest=''):
    '''
    发布文章到公众号
    :return:
    '''
    # 检测是否可以连接公众号
    my_wechat = wechat.WeChat()
    # 获得数据
    data = finance.fetch_all(target_config, config.kline_num)
    # 生成图片
    kline.generate_all_picture(target_config, data)
    # 上传图片
    my_wechat.upload_thumb(config.path_thumb_picture)
    url_list = my_wechat.upload_picture(target_config)
    # 生成文章
    article = wechat.generate_article(url_list)
    if title == '':
        title = config.wechat_title
    if author == '':
        author = config.wechat_author
    if digest == '':
        digest = config.wechat_digest
    my_wechat.generate_data(title, article, author, digest)
    # 上传文章
    my_wechat.send_requests()

def publish_article():
    '''
    发布文章
    :return:
    '''
    # 获取最后的草稿id
    my_wechat = wechat.WeChat()
    media_id = my_wechat.get_newest_draft()
    # 发布草稿
    #my_wechat.submit_draft(media_id)
    # 群发草稿
    my_wechat.sendall(media_id)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("please input arg\n")
    arg = sys.argv[1]
    if arg == "upload":
        if len(sys.argv) == 5:
            upload_article(sys.argv[2], sys.argv[3], sys.argv[4])
        elif len(sys.argv) == 2:
            upload_article()
        else:
            raise Exception("arg error\n")
    elif arg == "publish":
        publish_article()
    else:
        raise Exception("arg error\n")
