import requests

cookies = {
    'ASPSESSIONIDQWTDSQTT': 'LHBCPDMDHGKGJHBJIOLPCLKA',
    '__root_domain_v': '.zdaye.com',
    '_qddaz': 'QD.899112294458810',
    '_qddab': '3-mc5oow.lumjul04',
    'lastSE': 'google',
    'ASPSESSIONIDQWTCRSTT': 'JLNPPBNDAFAFOIFGEPDIHLAB',
    'ASPSESSIONIDSURCSQST': 'DKADBAODJIHPPIKMJICEGLDK',
    'acw_tc': '0a472f9217123145025678546e00586cfe3d84bef11b9fb2b553076b163dc6',
    '_qdda': '3-1.1',
    'ASPSESSIONIDSURDRSSS': 'AMINBOODMLEBPBPKHMIMNHEH',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASPSESSIONIDQWTDSQTT=LHBCPDMDHGKGJHBJIOLPCLKA; __root_domain_v=.zdaye.com; _qddaz=QD.899112294458810; _qddab=3-mc5oow.lumjul04; lastSE=google; ASPSESSIONIDQWTCRSTT=JLNPPBNDAFAFOIFGEPDIHLAB; ASPSESSIONIDSURCSQST=DKADBAODJIHPPIKMJICEGLDK; acw_tc=0a472f9217123145025678546e00586cfe3d84bef11b9fb2b553076b163dc6; _qdda=3-1.1; ASPSESSIONIDSURDRSSS=AMINBOODMLEBPBPKHMIMNHEH',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

params = {
    'ip': '',
    'adr': '',
    'checktime': '3',
    'sleep': '2',
}

response = requests.get('https://www.zdaye.com/free/', params=params, cookies=cookies, headers=headers)

print(response.text)