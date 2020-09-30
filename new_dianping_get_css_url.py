import requests
import re
from bs4 import BeautifulSoup


def get_d(url, id, cookie):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': cookie,
        'Host': 'www.dianping.com',
        'Referer': 'http://www.dianping.com/shop/' + id + '/review_all',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    with open('source.txt', 'w', encoding='utf-8')as f:
        f.write(r.text)
    url_css = 'http:' + \
              re.findall(r'<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.net/v1/.*?.css)">', r.text)[0]
    # print(url_css)
    headers_css = {
        'Host': 's3plus.meituan.net',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    r_css = requests.get(url_css, headers=headers_css)
    svg_url = 'https:' + re.findall(r'background-image: url\((//s3plus.meituan.net/v1/.*?.svg)\)', r_css.text)[-1]
    # print(svg_url)
    headers_svg = {
        'authority': 's3plus.meituan.net',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    r_svg = requests.get(svg_url, headers=headers_svg)
    soup = BeautifulSoup(r_svg.text, 'lxml')
    path = soup.find_all('path')
    textPath = re.findall(r'<textPath.*?>(.*?)</textPath>', r_svg.text)
    print(len(path), len(textPath))
    d = []
    for p in zip(path, textPath):
        id = p[0]['id']
        dl = p[0]['d'].split(' ')[1]
        txt = p[1]
        d.append([dl, txt])

    print(d)
    return d


if __name__ == '__main__':
    url = 'http://www.dianping.com/shop/22012462/review_all'
    d = get_d(url, '22012462',
              cookie='__mta=147617416.1566452719397.1566452719397.1566452719397.1; cy=1; cityid=1; cye=shanghai; _lxsdk_cuid=16ca95b04a8c8-0973a1b7a04c99-c343162-144000-16ca95b04a9c8; _lxsdk=16ca95b04a8c8-0973a1b7a04c99-c343162-144000-16ca95b04a9c8; s_ViewType=10; citypinyin=xiamen; cityname=5Y6m6Zeo; _tr.u=hUIIyezhEuprQEu1; ua=dpuser_0704841770; _hc.v=3be033b4-0be6-da29-c19e-c862ffbf2657.1600830012; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1600830012; ll=7fd06e815b796be3df069dec7836c3df; ctu=83e797fda01339a41ad3474928b9edd49a45958b8ceb4a8511bd61768d9790a6; uamo=15817121790; fspop=test; cy=4; cye=guangzhou; dper=eb48641fac70455fd7f2f6e10ecd47ce3eee6096612de0696eaf59aafbb7c8bdc75c2cc094c34cb05324d3b53d350cda2d993dcc73bded6f2646a08d744e1fee2de30a68b43330ec12e770bca0d6f459bd1fabbd94e353fc4edd62a705e87125; dplet=411e670fc83676a0a74997944c0c1d2b; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1600868024; _lxsdk_s=174bb1a8417-4c7-00a-ec1%7C%7C232')
