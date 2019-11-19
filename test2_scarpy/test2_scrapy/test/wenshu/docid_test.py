import execjs







key = """
BcOBw4kBAEEEBMOAwpTCmmHDsXTDph/DklbCjcOLwoJEUcKDw57DmVgUw7xaSxVmw6zDsSzCv10kwq/CvcKPY8OIwqIZwq3DvMKpDMORw43CusO4HcKXw5E5acOyW8KreHXCiMKRd8Oqwo7CoC0PKMOuwojDucONwpPCtUl4ZMO3K1HCsU/DhzAmwpTCoMKlw67DoMOlR35uXcOZZsKRwr4GWVLDjnRlwqrDrwLCnMOSVTLDlsOfwo1Gw4VHIsK4w4rDoBsuwqTDng8=
"""
id = 'DcOOw4kNADEIBMOBwpQ4wowZwp7DpsOKP8Kkw513S8KlTsK8wpzCriUbw5how58hGgzDqGrDkwk+wqHDm3kiD8OVOg9YQyhmXcOWw5UOw5I5w4pbRcKUwqXDq8OYwovDsGXCvzJ7w6FVXGwSGWk9YcKxZVNOw6/CjcKOw4srwqjDlEHDg8OjTcKnw7xywrR4w6TDusO9N8OAe8K2w4ByNwXCgHYuwqXCjmI0w7nDrk91w7fDgVPDmAPDvTXDvsKmGVZjw5pyPw=='

# with open('list.js', encoding='utf8') as f:
#     file = f.read()
#     ctx = execjs.compile(file)
#     r = ctx.call('Navi', id, '')
#     print(r)

# with open('docid_new.js') as fp:
#     js = fp.read()
#     ctx2 = execjs.compile(js)
#
#
# docid = ctx2.call("DecryptDocID", key, id)
# print(docid)
# print(1)

with open('vl5x_new.js') as fp:
    js = fp.read()
    ctx = execjs.compile(js)

def get_vl5x(vjkl5):
    """
    根据vjkl5获取参数vl5x
    """
    vl5x = (ctx.call('GetVl5x',vjkl5))
    return vl5x

v = 'fa7fe98ffeceeae010f18463878fe040824bc058'
print(get_vl5x(v))