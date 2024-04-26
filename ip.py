# encoding:utf-8
import re
import chardet
from random import choice
import asyncio
import requests
import sys
import random
from pyppeteer import launch
from aiohttp import ClientSession, ClientTimeout, TCPConnector
# import encodings.idna


path = '/root/momo-share-cpp/ip.txt'  # 文件保存地址


# 随机返回请求头
async def getheaders():
    headers_list = [
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8L1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8J2",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8J2 Twitter for iPhone",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8L1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8J3",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8L1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8J2",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; sv-se) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ko-kr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; it-it) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-fr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; es-es) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-gb) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; de-de) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36", ]
    headers = {'User-Agent': choice(headers_list)}
    return headers


# 清空文档
def clear_file():
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()

# 写入文档
async def record(text):
    with open(path, 'a', encoding='utf-8') as f:
        text = text + '\n'
        f.write(text)

async def getHtmlWithRunJs(url):
    print('启动浏览器')
    browser = await launch(executablePath='/opt/google/chrome/google-chrome',headless=True,args=['--no-sandbox'])
    # 打开一个新页面
    page = await browser.newPage()
    # 开启js
    await page.setJavaScriptEnabled(enabled=True)
    # 设置请求头
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
    )
    # 开启 隐藏 是selenium 让网站检测不到
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.setViewport(viewport={"width": 1920, "height": 1080})
    # 访问指定URL
    await page.goto(url)
    # 等待页面加载完毕，示例中等待了2秒
    await asyncio.sleep(2)
    # 获取页面内容
    content = await page.content()
    # 关闭浏览器
    await browser.close()
    return content

# 实例化请求对象
async def create_aiohttp():
    # 实例化对象
    async with ClientSession() as session:
        task = [
            asyncio.create_task(get_page('http://www.kxdaili.com/dailiip/2/1.html',mod=2, session=session)),
            asyncio.create_task(get_page('https://www.zdaye.com/free/?ip=&adr=&checktime=3&sleep=2',mod=2, session=session,isUseJs = 1)),
            asyncio.create_task(get_page('https://www.kuaidaili.com/free', mod=2, session=session,isUseJs = 1)),
            asyncio.create_task(get_page('https://www.kuaidaili.com/free/fps/', mod=2, session=session,isUseJs = 1)),
            asyncio.create_task(get_page('http://www.66ip.cn/mo.php?sxb=&tqsl=50',mod=0, session=session)),
            asyncio.create_task(get_page('https://www.89ip.cn',mod=1, session=session)),
            #asyncio.create_task(get_page('http://v2.api.juliangip.com/dynamic/getips?auto_white=1&filter=1&num=50&pt=1&result_type=text&split=2&trade_no=1692062021098359&sign=fee2bf9b19c1ddb225efd8a41c9d3185',mod=1, session=session)),
            #asyncio.create_task(get_page('https://cdn.jsdelivr.net/gh/parserpp/ip_ports@master/proxyinfo.txt',mod=0, session=session)),
            #asyncio.create_task(get_page('https://fastly.jsdelivr.net/gh/parserpp/ip_ports@main/proxyinfo.txt',mod=0, session=session)),
            asyncio.create_task(get_page('https://www.proxy-list.download/api/v1/get?type=http', mod=3, session=session)),
        ]

        for i in range(1, 4):
            task.append(asyncio.create_task(get_page(f'https://proxy.ip3366.net/free/?action=china&page={i}',mod = 2, session=session)))
            task.append(asyncio.create_task(get_page(f'http://www.kxdaili.com/dailiip/1/{i}.html',mod=2, session=session)))
            task.append(asyncio.create_task(get_page(f'http://ip.tyhttp.com/{i}/',mod=2, session=session)))
        await asyncio.gather(*task)


# 访问网页
async def get_page(url, session, mod=0 ,isUseJs = 0):
    hd = await getheaders()  # 请求头
    try:
        if isUseJs:
            page_source = await getHtmlWithRunJs(url)
            ip_lists = await soup_page(page_source, mod=mod)
            for ip in ip_lists:
                        await record(ip)
            print(f"['{url}']抓取成功{len(ip_lists)}个")
            return
        async with await session.get(url=url, headers=hd, timeout=20) as response:
            data = await response.read()  # 返回字符串形式的相应数据
            encoding = chardet.detect(data)['encoding']
            #print(f'page detected  possible encoding:{encoding}')
            encodings = [encoding ,'utf-8', 'gbk', 'GB2312', 'windows-1252']  # 常见编码列表
            for encoding in encodings:
                try:
                    page_source = data.decode(encoding)
                    #print(page_source)
                    ip_lists = await soup_page(page_source, mod=mod)
                    #await check_proxtList(ip_lists)
                    for ip in ip_lists:
                        await record(ip)
                    #print(f"['{url}']成功解码：{encoding}")
                    print(f"['{url}']抓取成功{len(ip_lists)}个")
                    break
                except UnicodeDecodeError:
                    print(f"['{url}']解码失败：{encoding}")
                    continue
    except Exception as e:
        print(f"['{url}']抓取失败:", e)


# 清洗页面 提取IP
# 生成代理链接格式: http://ip:port
async def soup_page(source, mod):
    ip_list = []
    if mod == 0:
        # 通用
        # 正则表达式匹配IP地址及端口号
        # \d{1,3} 匹配1到3位数字，\.:匹配点号。
        # :\d{1,5} 匹配冒号和其后的1到5位数字（端口号范围）。
        ip_port = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\b', source)
        for i in ip_port:
            ip_list.append(f"http://{i}")

    elif mod == 1:
        # 89ip.cn
        ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)', source)
        posts = re.findall(r'\s(\d{1,5})\s', source)
        for i in range(len(ips)):
            ip_list.append(f"http://{ips[i]}:{posts[i]}")

    elif mod == 2:
        # 快代理 || kxdaili.com || proxy.ip3366.net || http://ip.tyhttp.com/3/
        ips = re.findall(r'>(\d+\.\d+\.\d+\.\d+)</', source)
        posts = re.findall(r'>(\d{2,5})</', source)
        for i in range(len(ips)):
            ip_list.append(f"http://{ips[i]}:{posts[i]}")

    elif mod == 3:
        # www.proxy-list.download/api/v1/get?type=http
        ip_port = source.split('\r\n')[:-1]
        for i in ip_port:
            ip_list.append(f"http://{i}")
    random.choices(ip_list)
    return ip_list



def ip_main():
    clear_file()  # 清空存放代理文件
    print('正在抓取代理ip。。。')
    # 所有任务完成后关闭客户端会话和事件循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_aiohttp())
    print("代理抓取完成!!!")

ip_main()