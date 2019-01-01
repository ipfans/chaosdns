import os
import time
from typing import List, Optional

import requests_html
from yarl import URL

sess = requests_html.HTMLSession()
sess.headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
special_domain = ["com.cn", "gov.cn"]


def random(max: int) -> int:
    size = max // 256
    if max % 256 > 0:
        size += 1
    return int.from_bytes(os.urandom(size), byteorder="little") % max


def fix_url(url: str, domain: str) -> str:
    host: str = URL(domain).host
    if url.startswith("http"):
        return url
    if url.startswith("//"):
        url = "https:" + url
    elif url.startswith("/"):
        url = "https://" + host + url
    else:
        url = f"https://{host}/{url}"
    return url


def base_domain(url: str) -> str:
    host = URL(url).host
    if host is None:
        return ""
    offset = -2
    for sd in special_domain:
        if host.endswith(sd):
            offset = -3
    try:
        return ".".join(host.split(".")[offset:])
    except Exception:
        return host


def spider(url: str) -> None:
    try:
        print(url)
        r = sess.get(url)
        domain = base_domain(url)
        urls = []
        for link in r.html.links:
            link: str = fix_url(link, url)
            if base_domain(link) == domain:
                urls.append(link)
        urls = list(set(urls))
        rand = []
        max = random(8) + 5
        for i in range(max):
            rand.append(urls[random(len(urls))])
        rand = list(set(rand))
        for url in rand:
            print(url)
            time.sleep(1 + random(9))
            sess.get(url)
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    with open("site.txt", "r") as f:
        site: List[str] = f.readlines()
        while True:
            i = random(len(site))
            spider(site[i].replace("\n", ""))
            time.sleep(1 + random(9))
