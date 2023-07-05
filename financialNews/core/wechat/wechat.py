from urllib import parse, request
import json

import requests

from financialNews.config import config
from financialNews.utils import util

class WeChat():
    def __init__(self, token=''):
        self.appID = config.appID
        self.appsecret = config.appsecret
        self.data = {}
        self.thumb_media_id = ''
        if token == '':
            self.access_token = self.generate_token()
        else:
            self.access_token = token
        print("access token ......." + self.access_token)

    def generate_token(self):
        textmod = {"grant_type": "client_credential",
                   "appid": self.appID,
                   "secret": self.appsecret
                   }
        textmod = parse.urlencode(textmod)
        try:
            req = request.Request(url='%s%s%s' % (config.token_url, '?', textmod), headers=config.header)
            res = request.urlopen(req)
            res_decode = res.read().decode(encoding='utf-8')
            print(res_decode)
            res_json = json.loads(res_decode)
            print(res_json)
            '''
            errmsg:
            1, IP白名单
            '''
            errmsg = res_json.get("errmsg", "none")
            if errmsg != "none":
                raise Exception(errmsg)
        except Exception as err:
            print('An exception happened when generate token' + str(err))
        else:
            access_token = res_json["access_token"]
            return access_token

    def upload_material(self, path_picture, pic_type):
        """
        上传图片
        :param path_picture:
        :param pic_type: thumb 缩略图
        :return:
        """
        url = config.add_material_url + f"access_token={self.access_token}&type={pic_type}"
        print(url)
        with open(path_picture, 'rb') as fp:
            files = {'media': fp}
            res = requests.post(url, files=files)
            res_json = json.loads(str(res.content, 'utf-8'))
            print(res_json)
            media_id = res_json["media_id"]
            media_url = res_json['url']
        return media_id, media_url

    def upload_thumb(self, path_picture):
        '''
        上传缩略图
        :param path_picture:
        :return:
        '''
        media_id, media_url = self.upload_material(path_picture, 'thumb')
        self.thumb_media_id = media_id

    def upload_picture(self, target_config):
        '''
        上传文章内图片
        :param target_config:
        :return:
        '''
        url_list = []
        for target in target_config:
            file_path = config.dir_picture + util.get_date_str() + target[0] + '.png'
            media_id, media_url = self.upload_material(file_path, 'image')
            url_list.append(media_url)
        return url_list

    def generate_data(self, title, content, author='', digest=''):
        article = {
            "title": title,
            "content": content,
            "thumb_media_id": self.thumb_media_id
        }
        if author != '':
            article["author"] = author
        if digest != '':
            article["digest"] = digest
        self.data = {"articles": [article]}

    def send_requests(self):
        '''
        发送数据
        :return:
        '''
        try:
            response = requests.post(
                url=config.draft_url,
                params={'access_token':self.access_token},
                headers=config.header,
                data=bytes(json.dumps(self.data, ensure_ascii=False).encode('utf-8'))
            )
            obj = json.loads(response.content)
            return obj['media_id']
        except Exception as e:
            print(e)

    def get_newest_draft(self):
        data = {"offset":0, "count":1, "no_content":1}
        response = requests.post(
            url=config.get_draft_list_url,
            params={'access_token':self.access_token},
            headers=config.header,
            data=bytes(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        )
        obj = json.loads(response.content)
        update_time = obj["item"][0]['update_time']
        print("update_time :" + str(update_time))
        if not util.same_day_as_today(update_time):
            raise Exception("draft not same day as today")
        return obj["item"][0]["media_id"]

    def submit_draft(self, media_id):
        data = {"media_id":media_id}
        response = requests.post(
            url=config.submit_url,
            params={'access_token': self.access_token},
            headers=config.header,
            data=bytes(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        )
        obj = json.loads(response.content)
        if obj['errcode'] != 0:
            raise Exception("submit draft error")

    def sendall(self, media_id):
        data ={
            "filter": {"is_to_all": False, "tag_id": 2},
            "mpnews": {"media_id": media_id},
            "msgtype": "mpnews",
            "send_ignore_reprint": 0
        }
        response = requests.post(
            url=config.sendall_url,
            params={'access_token': self.access_token},
            headers=config.header,
            data=bytes(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        )
        obj = json.loads(response.content)
        print(obj)
        if obj['errcode'] != 0:
            raise Exception("send all error")

def generate_article(url_list):
    f = open(config.path_example_html, "r", encoding="utf-8")
    content = f.read()
    f.close()
    for url in url_list:
        content = content + f'<img src="{url}">' + "\n"
    content = content + "</body>\n</html>"
    return content
            
            

