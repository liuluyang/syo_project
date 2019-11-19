


def check_content(content):
    check_list = ['《币世界》']
    for w in check_list:
        content = content.replace(w, '')

    return content


content = """
据《币世界》最新行情，BTC小幅拉升，创日内新高达7674美元。火币现报7666美元，涨幅0.85%。

"""

if __name__ == '__main__':
    print (check_content(content))