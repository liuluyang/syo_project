import requests

def register():
    data = {"name":"小刘", "password":"123"}
    req = requests.post('http://127.0.0.1:9001/demo/register/', data=data).json()


    print(req, type(req))

def login():
    data = {"phone_num": "15076157670", "password": "654321"}
    req = requests.post('http://127.0.0.1:9001/demo/login_app/',
                        data=data)
    data = req.json()

    print(data, type(data), req.cookies.items())

#login()

def logout():
    #data = {"name": "小刘", "password": "123"}
    cookies = {"sessionid":"jpn8eu8cqcfiva93zq7gm8fd904kuubq"}
    req = requests.post('http://127.0.0.1:9001/demo/logout_app/', cookies=cookies)
    data = req.json()

    print(data, type(data), req.cookies)

#logout()

def register_by_phone():
    data = {"phone_num":"15076157670"}
    #data = {"phone_num":"15076157670", "code_num":"887979", "password":"123456"}
    req = requests.post('http://127.0.0.1:9001/demo/register_app/',
                        data=data)
    data = req.json()

    print(data, type(data), req.cookies.items())

#register_by_phone()

def reset_password_app():
    data = {"phone_num":"15076157670"}
    data = {"phone_num":"15076157670", "code_num":"351856", "password":"654321"}
    req = requests.post('http://127.0.0.1:9001/demo/reset_password_app/',
                        data=data)
    data = req.json()

    print(data, type(data), req.cookies.items())

#reset_password_app()

