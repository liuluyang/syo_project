import requests

cok = [('__cfduid', 'd417ec2d257cd3aade8f4639c46601f851538191233'),
       ('ASP.NET_SessionId', 'kukeqaxewzqxrcdu0wipcg3l'),
       ('__cflb', '3229817113')]
cookies = {k:v for k,v in cok}
print (cookies)
r = requests.get('https://etherscan.io/token/0xB8c77482e45F1F44dE1745F52C74426C631bDD52',
                 cookies=cookies)

print (r)