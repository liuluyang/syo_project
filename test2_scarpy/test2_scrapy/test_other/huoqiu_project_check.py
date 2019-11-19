





def check_content(content):
    check_list = ['来源：Biknow.com']
    for w in check_list:
        content = content.replace(w, '')

    return content


content = """
Genaro Network(GNX)7月份月报发布。来源：Biknow.com

"""

if __name__ == '__main__':
    print (check_content(content))