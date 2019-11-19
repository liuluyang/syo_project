import execjs


with open('test.js', 'r') as f:
    p = f.read()
    cxt = execjs.compile(p)
    print(cxt.call('add', 1 ,2))