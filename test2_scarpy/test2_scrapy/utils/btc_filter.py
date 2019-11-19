from scrapy import Selector

def delete_img_attr(tag):
    check = ['原文：' ,'作者：']
    text = Selector(text=tag)
    print (text)

    for c in check:
        if c in tag:
            return ''

    if text.css('img'):
        class_value = text.css('img::attr(class)').extract()
        width = text.css('img::attr(width)').extract()
        height = text.css('img::attr(height)').extract()
        for c in class_value:
            tag = tag.replace( 'class="' + c +'"', "")
        for w in width:
            tag = tag.replace( 'width="' + w +'"', "")
        for h in height:
            tag = tag.replace( 'height="' + h +'"', "")

    return tag

content = ['<p>韩国政府公布了税法修正案。新的税法规定，比特币交易所将不再和中小企业共同享有所得税和公司税的减免优惠。另外，监管部门还考虑对出售加密货币的行为征收资本利得税。</p>',
           '<p><img class="aligncenter size-full wp-image-2"></p>']


if __name__ == '__main__':
    new = ''
    for con in content:
        new+=delete_img_attr(con)
    print (new)
    pass