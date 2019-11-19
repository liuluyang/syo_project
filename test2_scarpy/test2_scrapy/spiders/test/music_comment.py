
import scrapy
import json


class CommentSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['music.163.com']

    def start_requests(self):

        url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_189315?csrf_token='

        form_data = {
            'params': 'm33vnOKajYUelZxQ40mwkFr2tjakSwoIxtClhVEuVMO6DxQKBEhRjDclZFFHj + AOytDDQ1PrNauvtH3phM + pz / '
                      'm65NG6m72xzG3pYB97w + LAOdNALCdusgtXj3TTvJ + OPiAiYGT + lu6 / p7DtqUIVYZNkEGTW9riW8JW9XYSvRsHz36qp8Vg4kWDNEQzkBKTc',
            'encSecKey': '2a6f7c9cddc8a847e74be9c89552ddb42c433eba18b51a94f5e0f4f2d2d108fb79ed1575fa13868d2a3b'
                         '57496de861d75c12f000d4f822313cccd90d51468e2b3feeb43e8950f34e135d6b99f9a5e0f5a40cf605c81707ffb6c'
                         '3939e0754d473bb8259e9186c651f9ae51e7c6bf36f9c7c09ae8b76c49110558c7870761d2487'
        }

        yield scrapy.FormRequest(url, callback=self.parse, formdata=form_data)

    def parse(self, response):

        data = json.loads(response.text)
        hot_comments = data.get('hotComments')

        #print (hot_comments)

        for num, per in enumerate(hot_comments):
            print (num, per['content'])
            if per.get('beReplied'):
                for i in per.get('beReplied'):
                    print ('回复：',i['content'])

