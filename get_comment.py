import requests
import re
from bs4 import BeautifulSoup
import demjson
from new_dianping_get_css_url import get_d
from openpyxl import Workbook
from openpyxl import load_workbook
import time
import random
from tqdm import tqdm


def get_css(source):
    url_css = 'http:' + \
              re.findall(r'<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.net/v1/.*?.css)">', source)[0]
    print(url_css)
    headers_css = {
        'Host': 's3plus.meituan.net',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    r_css = requests.get(url_css, headers=headers_css)
    return r_css.text


def get_data(shopid, cookie):
    global total
    wb = Workbook()
    ws = wb.active
    ws.append(['商家id', '评论id', '用户昵称', '评分', '评价', '评论', '时间'])
    outbreak = False
    for page in tqdm(range(1, 99)):
        url = 'http://www.dianping.com/shop/' + shopid + '/review_all/p' + str(
            page) + '?queryType=sortType&queryVal=latest'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': cookie,
            'Host': 'www.dianping.com',
            'Referer': 'http://www.dianping.com/shop/' + shopid + '/review_all',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        if '请求正常，是数据/页面不正常' in r.text:
            break
        class_data = get_css(r.text)
        d = get_d(url, shopid, cookie)
        # print(d)
        soup = BeautifulSoup(r.text, 'lxml')
        lis = soup.find('div', class_='reviews-items').find('ul').find_all('li', class_='')
        if len(lis) == 0:
            break
        print('===============================', page, '===============================')
        for li in lis:
            main_block = li.find('div', class_='main-review')
            name = main_block.find('a', class_='name').text.replace(' ', '').replace('\n', '')
            try:
                stars = main_block.find_all('span', class_='star')[0]['class'][1].replace('sml-str', '')
            except:
                stars = '0'
            time_ = main_block.find_all('span', class_='time')[0].text.strip()
            if time_ < '2019-09-01 00:01':
                outbreak = True
                break
            comment_id = main_block.find_all('a', class_='praise')[0]['data-id']
            try:
                scores = [i.text.replace(' ', '').replace('\n', '') for i in
                          main_block.find('span', class_='score').find_all('span')]
            except:
                scores = []
            comment = li.find('div', class_='review-words').contents
            msg = []
            for each in comment:
                txt = each
                if 'svgmtsi' in str(each):
                    result = re.findall(each['class'][0] + '\{(.*?)\}', class_data)[0]
                    x = float(result.split(':')[1].split(' ')[0].replace('-', '').replace('px', ''))
                    y = float(result.split(':')[1].split(' ')[1].replace('-', '').replace('px;', ''))
                    index_x = int(x / 14)
                    for d_item in d:
                        if y > int(d_item[0]):
                            continue
                        else:
                            txt = d_item[1][index_x]
                            break
                if type(each) != str:
                    pass
                msg.append(txt)
            s = ''
            for msg_item in msg:
                if isinstance(msg_item, str):
                    s = s + msg_item.replace(' ', '').replace('\n', '').replace('\t', '').replace('\xa0', '')

            # data = [name, stars, str(scores).replace('[', '').replace(']', '').replace("'", ''), s, time_]
            data = [shopid, comment_id, name, stars, str(scores).replace('[', '').replace(']', '').replace("'", ''), s,
                    time_]
            ws.append(data)
            total = total + 1
            print(total, data)
        if outbreak:
            break
        time.sleep(random.randint(8, 18))
    wb.save('./result/'+shopid + '.xlsx')


cookie = ''
shopid_list = [22011615]
total = 0
for s in tqdm(shopid_list):
    shopid = str(s)
    # try:
    get_data(shopid, cookie)
    time.sleep(random.randint(8, 18))
    # except:
    #     print(shopid)
    #     break
# page = 1
