import requests
import json
import time
import redis
import random
from scrapy.selector import Selector


"""
当抓取了十几个公众号文章历史列表之后，大概几万篇，微信该接口会显示操作频繁，
该帐号下无法再浏览历史列表。(禁封帐号24小时)
换个帐号可继续进行抓取操作。
"""

def redis_connection():
    """
    连接redis
    :return: 
    """
    pool = redis.ConnectionPool(host='47.75.223.85', port=6379, db=8, password='lvjian')
    r = redis.Redis(connection_pool=pool)

    return r


def data_redis(data):
    """
    报错记录
    :param data: 
    :return: 
    """
    r = redis_connection()
    time_now = time.strftime('%Y-%m-%d %X', time.localtime())
    data['updated_at'] = time_now
    data = json.dumps(data)
    r.lpush('error', data)


class WeixinArticle(object):

    def __init__(self, list_url):
        self.redis = redis_connection()
        self.list_url = list_url
        self.list_url_api = 'https://mp.weixin.qq.com/mp/profile_ext?' \
                            'action=getmsg&f=json&offset={offset}&count=10&' \
                            'is_ok=1&scene=123&'
        self.profile = {}
        headers = {
            #'Accept': 'text/html,application/xhtml + xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' #必填参数
        }
        session = requests.session()
        session.headers.update(headers)
        self.session = session

    def article_list_get(self):
        """
        公众号历史列表获取
        :return: 
        """
        if not self.profile_info_get():
            return False
        self.list_url_api += self.params_get()
        offset = 0
        while True:
            time.sleep(random.choice([0.5, 1, 1.5, 2]))
            data = {}
            try:
                resp = self.session.get(self.list_url_api.format(offset = offset))
                code = resp.status_code
                data_json = resp.json()
                if data_json.get('errmsg') == 'ok':
                    """
                    数据获取成功
                    """
                    data_list = json.loads(data_json['general_msg_list'])['list']
                    for d in data_list:
                        id = d['comm_msg_info']['id']
                        fakeid = d['comm_msg_info']['fakeid']
                        datetime = d['comm_msg_info']['datetime']
                        time_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.localtime(datetime))
                        app_msg = d.get('app_msg_ext_info')
                        if not app_msg:
                            continue
                        print(time_str)
                        print(app_msg['title'], app_msg['content_url'], app_msg['cover'])
                        data[app_msg['content_url']] = json.dumps({
                            'timestamp':datetime, 'time_str':time_str,
                            'title':app_msg['title'], 'content_url':app_msg['content_url'],
                             'cover':app_msg['cover']
                        })
                        for m in app_msg.get('multi_app_msg_item_list', []):
                            print(m['title'], m['content_url'], m['cover'])
                            data[m['content_url']] = json.dumps({
                                'timestamp': datetime, 'time_str': time_str,
                                'title':m['title'], 'content_url':m['content_url'],
                                'cover':m['cover']
                            })
                    if data:
                        self.redis.hmset(self.biz, data)
                        print('成功存入redis')
                    else:
                        print('本次请求无数据')
                else:
                    print('参数失效：', data_json)
                    error = data_json
                    data_redis(error)
                    break
            except Exception as e:
                print('请求错误：', e)
                error = {'error':str(e)}
                data_redis(error)
                break

            if data_json.get('msg_count') == 10:
                offset += 10
            else:
                print('数据抓取完成！')
                break

    def article_info_save(self, data):
        """

        :param data:
        :return:
        """

    def article_content_get(self, url):
        """
        获取文章正文
        :param url:
        :return:
        """

        html = self.session.get(url)
        print(html.text)
        pass

    def params_get(self):
        """
        公众号文章历史页url解析
        :return: 
        """
        params_list = self.list_url.split('&')
        params_str = ''
        params_need = ['__biz', 'uin', 'key', 'pass_ticket']
        for p in params_list:
            for p_n in params_need:
                if p_n in p:
                    params_str += '&' + p
        # print(params_str)

        return params_str

    def profile_info_get(self, is_check=1):
        """
        公众号信息获取
        :return: 
        """
        try:
            resp = self.session.get(self.list_url)
            resp = Selector(response=resp)
            biz = self.list_url.split('__biz=')[-1].split('&')[0]
            icon = resp.css('img#icon::attr(src)').extract_first().strip()
            title = resp.css('#nickname::text').extract_first().strip()
            desc = resp.css('p.profile_desc::text').extract_first().strip()
            print(title, desc, icon, biz)
            self.biz = biz
            if is_check:
                profiles = self.profiles()
                if biz in profiles:
                    print('该公众号已经抓取')
                    return False
            self.profile = {'biz':biz, 'nickname':title, 'desc':desc, 'avatar':icon}
            self.redis.hset('profile_info', biz, json.dumps(self.profile))
            return True
        except Exception as e:
            print('公众号profile数据获取失败：', e)
            error = {'error': str(e)}
            data_redis(error)
            return False

    def redis_data_get(self, biz):
        """
        获取某个公众号全部数据（redis）
        :param biz:
        :return:
        """
        data = self.redis.hgetall(biz)
        data = {k.decode():json.loads(v.decode()) for k,v in data.items()} if data else {}
        data = list(data.values())
        t = time.time()
        data.sort(key=lambda t:t['timestamp'], reverse=True)
        for v in data:
            print(v)

        print(time.time() - t)

    def profiles(self):
        """

        :return:
        """
        profiles = self.redis.hgetall('profile_info')
        profiles = {k.decode():json.loads(v.decode()) for k,v in profiles.items()} if profiles else {}
        for p in profiles.values():
            print(p)
        print(len(profiles))

        return profiles


if __name__ == '__main__':
    #url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAxMjUyNDQ5OA==&scene=123&uin=Mjk0NjU0NTgxNw%3D%3D&key=0a01442925ed28a193753e4c4b84b653d9b0b257682c3b2708a4f25ffcc22877b2f1a7e6d2981f2ecd1473c1bcd4827e801629ba6209d24485340cc5ab6a64bf76613d5a6a10b5f2d39a6150c6f8d749&devicetype=Windows+7&version=62060739&lang=zh_CN&a8scene=1&pass_ticket=hAyRfJTKbcaZGy0W1fi3vePQw0MKGNAQT8FajNwMVFeHeeIUpCgeYbiNmEP%2FT4kA'
    url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU1ODUxNDQ4NA==&scene=123&uin=MzY0MDEwMDM3Nw%3D%3D&key=f7985f301d8ef2f32f6aa0416795b148b55008637d0104f99bedd0476483d00d6c4371d8902942738ea7f5cafd9df6785ca88e6051be4ffa751e1eb0d29796ef4ded05d0775306ec898bcdfd8d9e0ce1&devicetype=Windows+10&version=62060833&lang=zh_CN&a8scene=1&pass_ticket=mTr8QDyZtnY3%2ByajdEqJOAdE4XaerGYG9PxoRqVyRYgcX74y68L3c2WSj0%2FEZ%2FCk'
    #url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU4MTUzMzMyNw==&scene=123&uin=Mjk0NjU0NTgxNw%3D%3D&key=0a01442925ed28a188f4d0e0a88d38e7ae90c334c5314e97188d45d1f0619e91eb96a9d57aacca68dc29e1f12b8d3f3f42430e6d2e1b69e9e5540c2f9ab44070aefb93f017ce71a817b2a72b44bf3244&devicetype=Windows+10&version=62060833&lang=zh_CN&a8scene=1&pass_ticket=1CJclwdNIYFv2lo6psCXJuSgShzmtdHttGIZhzUPBvC1VhUcJYD4ERNZvdh7T5Tr'
    w = WeixinArticle(url)
    # w.article_list_get()

    # w.article_content_get('https://mp.weixin.qq.com/s?__biz=MzA4MjEyNTA5Mw==&mid=2652569612&idx=1&sn=155bea0e33bb93f0b827128e98b9b988&chksm=84652846b312a1501f0a3ccfa651a7c13bc55884f24623d94e29793f9b78b12ed649c5a13ab6&scene=123#wechat_redirect')

    # w.redis_data_get('MzI1MDA2NjY2Nw==')

    w.profiles()











