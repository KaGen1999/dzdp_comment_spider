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
    svg_url = 'https:' + re.findall(r'background-image: url\((//s3plus.meituan.net/v1/.*?.svg)\)', r_css.text)[0]
    # print(svg_url)
    headers_svg = {
        'authority': 's3plus.meituan.net',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    r_svg = requests.get(svg_url, headers=headers_svg)
    soup = BeautifulSoup(r_svg.text, 'lxml')
    texts = soup.find_all('text')
    # print(texts)
    d = []
    for text_ in texts:
        d.append([text_['y'], text_.text])
    print(d)
    return d


if __name__ == '__main__':
    url = 'http://www.dianping.com/shop/2072497/review_all'
    d = get_d(url, '2072497')
