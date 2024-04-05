# encoding:utf-8
import asyncio
import sys
import os
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from ip import ip_main, getheaders
import random

# 可根据自己电脑更改位置
link_path = "/var/www/tools/momo-share/momo-share-proxy/Momo/momo_link.txt"


# 读取文件获取文件内容
def readfile():
    with open('ip.txt', 'r', encoding='utf-8') as file:
        ips = file.readlines()
    return ips


# 读取文件获取momo链接
def share_Link():
    # 判断文件是否存在，不存在则创建
    if os.path.isfile(link_path):
        fileopen = open(link_path, 'r', encoding='utf-8')
        momo_share_links = [i.strip() for i in fileopen.readlines()]
        # 判断是否有链接 无则终止程序
        if momo_share_links == []:
            fileopen.close()
            sys.exit()
        fileopen.close()
        return momo_share_links
    else:
        os.close(os.open(link_path, os.O_CREAT))  # 创建文件
        sys.exit()  # 终止程序


# 设置代理抓取https页面报错问题解决
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def create_aiohttp(url, proxy_list):
    random.choices(proxy_list)
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        # 生成任务列表
        task = [asyncio.create_task(web_request(url=url, proxy=proxy, session=session))
                for proxy in proxy_list]
        await asyncio.wait(task)


# 网页访问
async def web_request(url, proxy, session):
    global n 
    global cnt
    if n>25:
        print("n:",n)
        return
    print(f'次数{cnt}:{proxy}')
    cnt +=1
    hd = await getheaders()  # 设置请求头
    sem = asyncio.Semaphore(50)  # 设置限制并发次数.
    async with sem:
        try:
            async with await session.get(url=url, headers=hd, proxy=proxy, timeout=10) as response:
                # 返回字符串形式的相应数据
                page_source = await response.text()
                await page(page_source)
        except Exception as e:
            #print("网页请求失败! ", e)
            pass


global n  # 记录访问成功次数
global cnt


# 判断访问是否成功
async def page(page_source):
    global n
    if "学习天数" in page_source:
        n += 1
        print('访问成功!!!')


def main():
    links = share_Link()  # 读取文件里的墨墨分享链接
    print("访问链接:", links)
    #ip_main()  # 抓取代理
    proxies = [i.strip() for i in readfile()] # 生成代理列表
    for link in links:
        global n
        global cnt
        n = 0
        cnt = 0
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_aiohttp(link, proxies))
        print(f'[url:{link}]完成{n}次')
    print("任务完成!!!")


if __name__ == '__main__':
    main()
