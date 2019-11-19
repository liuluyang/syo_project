import json, requests
from urllib import parse
from lxml import etree
import redis
import time
import random


pool = redis.ConnectionPool(host='47.75.223.85', port=6379, db=9, password='lvjian')
redis_9 = redis.Redis(connection_pool=pool)
base_url = 'https://www.zhipin.com'
city = (('天津','c101030100'), ('合肥','c101220100'), ('青岛','c101120200'),
        ('郑州','c101180100'), ('南京','c101190100'), ('西安','c101110100'))
query = ['python', 'php']


def recruitment_list_get(c, q):
    """
    列表数据请求
    :param c:
    :param q:
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36',
    }
    url = 'https://www.zhipin.com/{}/?query={}&page={}'
    print(c, q)
    page = 1
    while True:
        r = requests.get(url.format(c[1], q, page), headers=headers)
        print(r)
        html = r.content.decode()
        # with open('index.html', 'w', encoding='utf8') as f:
        #     f.write(html)
        is_next = content_parse(html, c, q)
        if is_next < 30:
            break
        page += 1
        time.sleep(random.random())


def content_parse(content, c=None, q=None):
    """
    列表内容解析
    :param content:
    :return:
    """
    html = etree.HTML(content)
    info_list = html.xpath('//div[@class="job-list"]/ul/li')
    for li in info_list:
        title = li.xpath('.//div[@class="job-title"]/text()')
        red = li.xpath('.//span[@class="red"]/text()')
        p = li.xpath('.//p/text()')
        name = li.xpath('.//h3[@class="name"]/a/text()')[-1]
        detail_url = li.xpath('.//a/@href')[:2]
        # print(title, red, p, name, detail_url)
        data = (
            ('title', title[0]), ('red', red[0]), ('other', p), ('name', name),
            ('title_url', detail_url[0]), ('name_url', detail_url[-1]),
            ('city', c[0]), ('query', q)
        )
        data = dict(data)
        print(data)

        redis_9.hset('position', data['title_url'], json.dumps(data))

    print(len(info_list))

    return len(info_list)


def detail_content(title_url):
    """
    详情页信息抓取
    :param title_url:
    :return:
    """
    if redis_9.sismember('detail_set', title_url):
        print('%s详情页信息已经存在'%(title_url))
        return False

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'cookie':'sid=sem_pz_bdpc_dasou_title; __c=1563546129; __g=sem_pz_bdpc_dasou_title; _uab_collina=156354613053055793587714; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1563546131; lastCity=101030100; __l=l=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fDIFkY0IWPB0KZEgsDwYW7I00000Kd7ZNC00000pMNE5m.THdBULP1doZA8QMu1x60UWdVTLIGU-qEuydxuAT0T1dBm1R1uAcdnW0snjDLuh7W0ZRqPWnknRnYnWTdnH63nj03wjK7wjnLnj9AwDw7fbf3wWf0mHdL5iuVmv-b5HnznWfvnjf1Pj6hTZFEuA-b5HDv0ARqpZwYTZnlQzqLILT8Xh9GTA-8QhPEUitOTv-b5gP-UNqsX-qBuZKWgvw9TvqdgLwGIAk-0APzm1YkPH61r0%26tpl%3Dtpl_11534_19713_15764%26l%3D1511867677%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E5%252587%252586%2525E5%2525A4%2525B4%2525E9%252583%2525A8-%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253DBoss%2525E7%25259B%2525B4%2525E8%252581%252598%2525E2%252580%252594%2525E2%252580%252594%2525E6%252589%2525BE%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E6%252588%252591%2525E8%2525A6%252581%2525E8%2525B7%25259F%2525E8%252580%252581%2525E6%25259D%2525BF%2525E8%2525B0%252588%2525EF%2525BC%252581%2526xp%253Did(%252522m3224604348_canvas%252522)%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D8%26ie%3Dutf-8%26f%3D3%26tn%3Dmswin_oem_dg%26wd%3Dboss%25E7%259B%25B4%25E8%2581%2598%25E5%25AE%2598%25E7%25BD%2591%26rqlang%3Dcn%26inputT%3D4385%26prefixsug%3Dboss%26rsp%3D0&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title%26city%3D101030100; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1563546170; __a=50369149.1563546129..1563546129.4.1.4.4'
    }
    url = parse.urljoin(base_url, title_url)
    r = requests.get(url, headers=headers)
    if r.status_code in [404]:
        return None
    print(r, url)
    content = r.content.decode()
    # print(content)
    # with open('detail.html', 'w', encoding='utf8') as f:
    #     f.write(content)
    html = etree.HTML(content)
    text = html.xpath('//div[@class="job-sec"]/div/text()')
    text_new = ''
    for t in text:
        t =t.strip()
        if t:
            text_new += t + '\n'
    print(text_new)

    redis_9.hset('detail_dict', title_url, text_new)
    redis_9.sadd('detail_set', title_url)

    return text_new


def spider_main():
    """
    主程序
    :return:
    """
    for c in city[:]:
        for q in query[:]:
            recruitment_list_get(c, q)
            time.sleep(random.random())

def detail_main():
    """
    主程序
    :return:
    """
    # text_dict = redis_9.hgetall('detail_dict')
    # text_dict = {k.decode():v.decode() for k,v in text_dict.items()}
    # print(text_dict)
    # data = redis_9.hgetall('position')
    # json.dump({k.decode():v.decode() for k,v in data.items()}, open('data.txt', 'w'))
    data = json.load(open('data.txt', 'r'))
    for title_url in list(data.keys())[1950:]:
        # print(title_url)
        result = detail_content(title_url)
        if result == '':
            break
        time.sleep(random.random())


def data_merge():
    data_new = []
    data = json.load(open('data.txt', 'r'))
    data = {k:json.loads(v) for k,v in data.items()}
    data_detail = redis_9.hgetall('detail_dict')
    data_detail = {k.decode():v.decode() for k,v in data_detail.items()}
    print(type(data))
    for k,v in data.items():
        v.update({'detail':data_detail.get(k, '')})
        print(k,v)
        data_new.append(v)
    json.dump(data_new, open('boss_position.json', 'w'))
    # for k,v in data_detail.items():
    #     print(k,type(v), v)
    pass

def data_show():
    data = json.load(open('boss_position.json', 'r'))
    for index, d in enumerate(data):
        print(index, d)

if __name__ == '__main__':
    # spider_main()
    # with open('index.html', 'r', encoding='utf8') as f:
    #     content = f.read()
    # content_parse(content)
    #
    # detail_content('/job_detail/d2732df0257b26231XJ929q_GVo~.html')
    # detail_main()
    # data_merge()
    data_show()
    pass