
from scrapy.selector import Selector


text1  = "【实用干货技巧】高考语文突破140？语文学习方法论\n" \
         "<span class=\"url-icon\">" \
         "<img alt=\"[围观]\" src=\"//h5.sinaimg.cn/m/emoticon/icon/others/o_weiguan-440ebe5b66.png\" style=\"width:1em; height:1em;\"/>" \
         "</span> " \
         "<a data-url=\"http://t.cn/Req2VgR\" href=\"http://video.weibo.com/show?fid=1034:4266308364090063\" data-hide=\"\">" \
         "<span class='url-icon'>" \
         "<img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_video_default.png'>" \
         "</span>" \
         "<span class=\"surl-text\">高中辅导课日常的秒拍视频</span>" \
         "</a>"

text2 = "FCoin又放大招 FT1808到底能否助推FT币价_比特币_金色财经<br />今天FCoin推出的FT1808公告，经记者一番研究，其实是一条对FT币价利好的消息，但貌似好多人并没有看懂。<br /><a data-url=\"http://t.cn/Re2kSIG\" href=\"https://m.jinse.com/bitcoin/218522.html\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_web_default.png'></span><span class=\"surl-text\">网页链接</span></a> ​"
text3 = "比特币未来是什么？ <a data-url=\"http://t.cn/R2d2Ntw\" href=\"http://weibo.com/p/1001018008614072107000000\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_location_default.png'></span><span class=\"surl-text\">晋中·河峪乡</span></a> <a data-url=\"http://t.cn/RtLyBBZ\" href=\"http://video.weibo.com/show?fid=1034:06a6bb62d8546f93abf6b243da711d72\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_video_default.png'></span><span class=\"surl-text\">秒拍视频</span></a> . ​"
text4 = "小王子：“因为我倾听过你的沉默。”这个七夕，我在野兽派倾听你…诉说。<a href='/n/野兽派花店'>@野兽派花店</a>   <a  href=\"https://m.weibo.cn/p/searchall?containerid=231522type%3D1%26q%3D%23%E9%87%8E%E5%85%BD%E6%B4%BE%E5%8D%83%E7%8E%BA%E4%B8%83%E5%A4%95%23%26t%3D10&extparam=%23%E9%87%8E%E5%85%BD%E6%B4%BE%E5%8D%83%E7%8E%BA%E4%B8%83%E5%A4%95%23\" data-hide=\"\"><span class=\"surl-text\">#野兽派千玺七夕#</span></a> <a data-url=\"http://t.cn/ReyqRYb\" href=\"http://www.miaopai.com/show/2I-CcqX-8ZaFVukV94nyY65NdhI2P4b4ysFdEg__.htm\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_video_default.png'></span><span class=\"surl-text\">野兽派花店的秒拍视频</span></a> ​"
text5 = "有点像Fcoin新势力，来的太快了！//<a href='/n/克里斯托夫-金'>@克里斯托夫-金</a>:拼多多(PDD)剛剛在美成功上市，IPO價19，開盤價26.5，黃崢個人財富輕取劉強東夫婦，拼多多被普遍認為對阿裏巴巴和京東構成巨大威脅，如果PDD盈利前景看好，阿裏京東走下坡路，中國首富馬雲馬化騰將讓位。"
text6 = "为什么我今年没看世界杯？一张图总结世界杯\n<span class=\"url-icon\"><img alt=\"[允悲]\" src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_yunbei-c6964bf237.png\" style=\"width:1em; height:1em;\"/></span> <a data-url=\"http://t.cn/RJ2D8Qr\" href=\"http://weibo.com/p/1001018000200000000000061\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_location_default.png'></span><span class=\"surl-text\">加拿大·温哥华</span></a> ​"
text7 = "<a data-url=\"http://t.cn/RehVT7b\" href=\"https://m.xiaoyunquegroup.com/#/content/show/5b574dd40e3e397111d50189\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_web_default.png'></span><span class=\"surl-text\">网页链接</span></a>宝二爷：比特币不到100万美元直播吃鸡 ​"
text8 = "原本没有也就算了，一旦有了又被人抢走那便有了怒气，这时候就只需递给他一把趁手的武器。<br /><br />——鲁迅（没说过） <a data-url=\"http://t.cn/R2WxFX7\" href=\"http://weibo.com/p/1001018000200000000000000\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_location_default.png'></span><span class=\"surl-text\">加拿大</span></a> <a data-url=\"http://t.cn/Rg8QYIo\" href=\"http://video.weibo.com/show?fid=1034:4264217499391473\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_video_default.png'></span><span class=\"surl-text\">Bitangel宝二爷的微博视频</span></a> ​"
text9 = "<a href='/n/Waykichain维基链官方微博'>@Waykichain维基链官方微博</a> 本来就觉得你割韭菜太狠怼两句 你既然说我收黑钱 那么开始了 不要停\n<span class=\"url-icon\"><img alt=\"[摊手]\" src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_tanshou-dcf7d5d0d6.png\" style=\"width:1em; height:1em;\"/></span>\n<span class=\"url-icon\"><img alt=\"[摊手]\" src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_tanshou-dcf7d5d0d6.png\" style=\"width:1em; height:1em;\"/></span>\n<span class=\"url-icon\"><img alt=\"[摊手]\" src=\"//h5.sinaimg.cn/m/emoticon/icon/default/d_tanshou-dcf7d5d0d6.png\" style=\"width:1em; height:1em;\"/></span> <a  href=\"https://m.weibo.cn/p/index?extparam=%E6%AF%94%E7%89%B9%E5%B8%81&containerid=1008082cb931df4e46611edddff3b062bb1a73\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/1000/8/2018/04/20/super_default.png'></span><span class=\"surl-text\">比特币</span></a> <a  href=\"https://m.weibo.cn/p/index?extparam=%E5%8C%BA%E5%9D%97%E9%93%BE&containerid=10080875d8fafb0706c9381d4c91e3b184f19d\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/1000/8/2018/04/20/super_default.png'></span><span class=\"surl-text\">区块链</span></a> ​"
text10 = "<a data-url=\"http://t.cn/RggPMhW\" href=\"https://mp.weixin.qq.com/s?__biz=MzAxNzI4MTMwMw==&mid=2651632332&idx=1&sn=871c0a383e0548f43d4c12b780e7f4db&chksm=801feab4b76863a250a629b83ac26558728bf69922874c3cb8255fc05d9803d8402956ba97e3#rd&skey=@crypt_1b012ff8_d9900d4103baa30a26a2a706b7185d7e&deviceid=e839525045572447&pass_ticket=undefined&opcode=2&scene=1&username=@a1563a76934fccd6655edbb28667b03a\" data-hide=\"\"><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_web_default.png'></span><span class=\"surl-text\">“疫苗问题”与“无币区块链”技术</span></a> ​"

def content_parse(text):
    t1 = Selector(text="<div class='demon'>"+text+"​</div>")
    t1 = t1.xpath('//div[@class="demon"]/node()')
    text_new = []
    other_text = ''
    for t in t1:
        text = t.extract()
        alt = t.css('img::attr(alt)').extract_first()
        a = t.css('a::attr(href)').extract_first()
        if alt:
            text_new.append(alt)
        elif a:
            a_text = t.css('::text').extract_first()
            if '@' in a_text:
                text_new.append(a_text)
            else:
                other_text = a
        else:
            if '<br>' not in text:
                text_new.append(text)

    # print ('解析后的内容列表：')
    # print (text_new)
    # print (other_text)

    new_text = ''
    for t in text_new:
        new_text+=t.replace('\n','')

    if len(text_new)==1 and text_new[-1].strip().startswith('\u200b'):
        return other_text

    return new_text

if __name__ == "__main__":
    for num,text in enumerate([text1,text2,text3,text4,text5,text6,text7,text8,text9,text10]):
        print (num, content_parse(text))