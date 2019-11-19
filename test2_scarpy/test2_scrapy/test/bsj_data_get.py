import requests



url = "http://www.bishijie.com/kuaixun/?u_atoken=1536310050665.447&u_asession=01pFGGeJg8Omhpva1JUiFhxl4DSsLg74ATiPn5I3rA3oKt8BzIngWxKY4HJ5yt_7mGkI3UnYcm-T63UY9OfZBO7zy0klL_L-uP5_QiV1kb7zDCjkFKClHUsiwbEKwwAJxpXG-0K_alZy-Pu-TBWZUElP8lbKwpsg_p69EEEgH3xhl9blrKLMEsDxyHGtdbS8cH&u_asig=05-x9YJ76a-M7Yw93dZAP4tLYlpYyBwKCDxTsB-FihJquo7_KCWYX_NsIBy_cmAcQyl4wnxapFmcdGF8MRsq-3Vy4AZP3oBBPrdIYCX5b-ccOS2vE-WVBVB4_4RFapVnEOx2ujMD4nNGjTDz1trP8dSh9BvlK1CytwG1SjigqITAVItXABKCkJamvPZVgLU5v6CtqCwQXs11Zh5gcUiHNrkCA3CK5qvTRFVC9FlsjJfdyUMNB7cgI68mrZT4rmDwHxLz85TfCwqfkY23WOQQP3M4dkd8nvzuZ_0p_dqQejN2hdbJ9WjQG7wAEERkjU6IkLDNzt_VXLbe50rZ4BxVEPjoZQgIMSajJfABLQVFa03FoeRsVht-p5RXdIIs8864ADuj_r0ZDUxx5o14nClKpcnA&u_aref=undefined"
url_2 = 'http://www.bishijie.com/kuaixun/'


cookies = {
'token':'f1c133858152b19991ceab3cdca4a517',
    'user_info':'{%22user_id%22:1121936%2C%22show_id%22:211219367%2C%22openid%22:'
                'null%2C%22reg_type%22:0%2C%22access_token%22:null%2C%22unionid%22:'
                'null%2C%22uuid%22:%22web_pc%22%2C%22token%22:%22f1c133858152b1999'
                '1ceab3cdca4a517%22%2C%22mobile%22:%2215076157670%22%2C%22email%22:%2'
                '2%22%2C%22nickname%22:%22150****7670%22%2C%22wxnickname%22:null%2C%22'
                'sex%22:0%2C%22province%22:null%2C%22city%22:null%2C%22country%22:null%'
                '2C%22headimgurl%22:null%2C%22project_role%22:1%2C%22dynamic_num%22:0%2'
                'C%22follow_num%22:0%2C%22fans_num%22:0%2C%22invite_num%22:0%2C%22is_dis'
                'able%22:0%2C%22access%22:1%2C%22read_follow_max_article_id%22:0%2C%22praise_num%22:0%2C%22comment_num%22:0%2C%22banned_time%22:0%2C%22auth_tag1%22:%22%22%2C%22auth_tag2%22:%22%22%2C%22is_delete%22:0%2C%22enter_time%22:0%2C%22passwdStatus%22:0}',

'CNZZDATA1265004505':'1853842-1536309780-null%7C1536544403',
    'Hm_lvt_760519477a6dd9d6ef4ae6014436ab92':'1536205535,1536214091,1536310066,1536547314'
}

data = requests.get(url_2, cookies = cookies)

print (data.content.decode())
