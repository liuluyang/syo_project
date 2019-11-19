import re


#content = '据《币世界》监测，CNBC9月5日发文预测BTC会大涨后，9月5日下午5时起至现在，' \
          #'BTC出现几次大跌，下跌金额近1000美元。BTC现报价6404.86美元，跌幅8.48%。'
content = '据《币 世 界》监测，过去1小时推特币种讨论量排名中,BTC、TRX 和ETH位列前三，' \
          'XLM、BCH和EOS跻身前十。具体名单如下：BTC（2013次讨论量）、TRX（995）、' \
          'ETH（974）、XRP（615）、LTC（473）、NEO（401）、ADA（364）、EOS（360）、' \
          'BCH（355）和XLM（317）。'

def delete_word(text):
    word_list = re.findall(r'(《币.*世.*界》)', text)
    print (set(word_list))
    for i in set(word_list):
        text = text.replace(i, '')

    return text


if __name__ == '__main__':
    print (delete_word(content))