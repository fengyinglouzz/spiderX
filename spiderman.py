import requests
from bs4 import BeautifulSoup
import xlwt
import time
import re
import sys
import os


def get_cookies():
    with open("cookies.conf") as f:
        cookies_txt = f.readline()
        return cookies_txt

def totxt(datas, name):
    file_dir = os.path.split(os.path.realpath(__file__))[
                   0] + os.sep + "jiuzhaigou"
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    file_path = file_dir + os.sep + name + ".txt"
    f = open(file_path, "ab+")
    f.write((str(datas) + "\n").replace("\'", "\"").encode(sys.stdout.encoding))
    print(datas)


def toexcel(datas, name):
    wb = xlwt.Workbook(encoding='utf8')
    sheet = wb.add_sheet("Sheet 1")
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)

    sheet.write(0, 0, 'ID', style_heading)
    sheet.write(0, 1, '昵称', style_heading)
    sheet.write(0, 2, '是否认证', style_heading)
    sheet.write(0, 3, '发布终端', style_heading)
    sheet.write(0, 4, '位置', style_heading)
    sheet.write(0, 5, '位置链接', style_heading)
    sheet.write(0, 6, '日期', style_heading)
    sheet.write(0, 7, '时间', style_heading)
    sheet.write(0, 8, '微博内容', style_heading)
    data_row = 1
    for i in datas:
        sheet.write(data_row, 0, i["id"])
        sheet.write(data_row, 1, i["name"])
        sheet.write(data_row, 2, i["rz"])
        sheet.write(data_row, 3, i["from"])
        sheet.write(data_row, 4, i["address"])
        sheet.write(data_row, 5, i["address_href"])
        sheet.write(data_row, 6, i["date"])
        sheet.write(data_row, 7, i["time"])
        sheet.write(data_row, 8, i["content"])
        data_row = data_row + 1
    file_dir = os.path.split(os.path.realpath(__file__))[
                   0] + os.sep + "jiuzhaigou"
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    file_path = file_dir + os.sep + name + ".xls"
    wb.save(file_path)


def search(keyword=[], time="", page=1, file=""):
    key1 = keyword[0]
    url = "https://s.weibo.com/weibo?q=%s&scope=ori&suball=1&timescope=custom:%s&Refer=g&page=%s" \
          % (key1, time, page)
    res_list = []
    headers = {
        "Cookie": get_cookies(),
        "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.find_all("div", "card-feed")
    try:
        page_num = int(re.findall("\d+", soup.find("a", class_="pagenum").get_text())[0])
    except Exception as e:
        print(e)
        page_num = page
    if page_num != page:
        return []
    if "您可以尝试更换关键词，再次搜索" in res.text:
        return []
    for item in items:
        id_ = item.parent.parent.get("mid")
        name = item.find("a", class_="name").get_text()
        rz1 = item.find("i", class_="icon-vip icon-vip-y")
        rz2 = item.find("i", class_="icon-vip icon-vip-g")
        rz3 = item.find("i", class_="icon-vip icon-vip-b")
        content = item.find("div", class_="content").find("p", class_="txt").get_text().strip()
        icons = item.find_all("i", class_="wbicon")
        address = ""
        address_href = ""
        time_ = item.find("p", class_="from").a.get_text().strip()
        date = time_.split(" ")[0]
        try:
            time_ = time_.split(" ")[1]
        except Exception as e:
            print(e)
            time_ = ""
        try:
            from_ = item.find("p", class_="from").find_all("a")[1].get_text()
        except Exception as e:
            print(e)
            from_ = ""
        for icon in icons:
            if icon.get_text() == "2":
                address = icon.parent.get_text()[1:]
                address_href = icon.parent.get("href")
                if "http" in address_href:
                    new_address = requests.get(address_href, allow_redirects=False, headers=headers).headers["Location"]
                else:
                    new_address = requests.get("http:" + address_href, allow_redirects=False, headers=headers).headers["Location"]
                address_href = new_address

        if rz1 or rz2 or rz3:
            rz = "Yes"
        else:
            rz = "No"
        tmp = {
            "id": id_,
            "name": name,
            "rz": rz,
            "content": content,
            "address": address,
            "address_href": address_href,
            "time": time_,
            "date": date,
            "from": from_,
        }
        res_list.append(tmp)
        if len(keyword) > 1:
            if keyword[1] in content:
                totxt(tmp, file)
                res_list.append(tmp)
        else:
            totxt(tmp, file)
            res_list.append(tmp)
    return res_list


def redate(start, end):
    date_list = []
    start = int(time.mktime(time.strptime("20" + start, "%Y-%m-%d-%H")))
    end = int(time.mktime(time.strptime("20" + end, "%Y-%m-%d-%H")))
    while start < end:
        st = time.strftime("%Y-%m-%d-%H", time.localtime(start))
        et = time.strftime("%Y-%m-%d-%H", time.localtime(start + 3600))
        start += 3600
        date_list.append(st + ":" + et)
    return date_list


def run(keyword, start, end, file):
    date_list = redate(start, end)
    result = []
    for i in date_list:
        sys.stdout.write('\r正在获取%s的数据' % i)
        page = 1
        while True:
            time.sleep(0.5)
            res_list = search(keyword, i, page, file)
            if not res_list:
                break
            result += res_list
            page += 1
    # toexcel(result, file)


if __name__ == '__main__':
    run()
