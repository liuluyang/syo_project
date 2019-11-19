
import re

def delete_tag_a(text):
    a_list = re.findall(r'<a.*?>', text)
    print (set(a_list))
    for i in a_list + ['</a>']:
        text = text.replace(i, '')

    return text


if __name__ == '__main__':
    text = '<div><a href=""><span></span></a><a href=""></a></div>'
    print (delete_tag_a(text))