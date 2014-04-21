#coding=utf-8

import requests
from bs4 import BeautifulSoup as bs
import re

headers = {  # provide info for request
    'User-Agent': 'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)'
}


def baidu_url(word):  # construction baidu URL of serp
    """
    get baidu search url
    """
    return 'http://www.baidu.com/s?wd=%s' % word


def baidu_cont(url):  # baidu serp content
    r = requests.get(url, headers=headers)
    cont = r.content.replace('<b>', '').replace('</b>', '')
    return cont


def serp_links(word):  # return  baidu 10 serp links
    """
    get baidu serp links with the word
    """
    b_url = baidu_url(word)
    soup = bs(baidu_cont(b_url))
    b_tags = soup.find_all('h3', {'class': 't'})
    b_links = [tag.a['href'] for tag in b_tags]
    real_links = []
    for link in b_links:
        try:
            r = requests.get(link, headers=headers, timeout=120)
        except Exception as e:
            real_links.append('page404')
        else:
            real_links.append(r.url)
    return real_links


def cache_links(word):  # return 10 cache links in baidu serp
    """
    get cache links in baidu serp
    """
    b_url = baidu_url(word)
    soup = bs(baidu_cont(b_url))
    b_tags = soup.find_all('span', {'class': 'g'})
    b_links = [tag.string for tag in b_tags]
    return b_links


def indexer(url):  # check is whether indexed or not
    indexed_links = serp_links(url)
    if url in indexed_links:
        return True
    else:
        return False


def simple_indexer(url):  # check baidu index status simply
    caches = cache_links(url)
    url = url.replace('http://', '')[:16]
    print url
    print caches
    for c in caches:
        if url in c:
            return True
            break
    else:
        return False


def siter(word):  # check the num of baidu site
    word = 'site:' + word
    b_url = baidu_url(word)
    soup = bs(baidu_cont(b_url))
    div_tag = soup.find('div', {'class': 'c-span21 c-span-last'})
    b_res = div_tag.p.string
    pat = re.compile(r'[0-9,]+')
    match = pat.search(b_res)
    if match:
        return match.group()
    else:
        return 'no data'


def ranker(word, url):  # check baidu rank with 100% accuracy
    serps = serp_links(word)
    for num, link in enumerate(serps):
        if url in link:
            return num + 1
            break
    else:
        return 'no data'


def simple_ranker(word, url):  # check baidu rank simply
    caches = cache_links(word)
    for num, link in enumerate(caches):
        if link is None:
            continue
        elif url in link:
            return num + 1
            break
    else:
        return 'no data'


