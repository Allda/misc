import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "http://pis.org.pl"
search_url = "http://pis.org.pl/aktualnosci?search=&sort=oldest&tag=&"

max_index = 53

keywords = ["brexit", "brytan", "brytyj", "cameron", "ue", "unia", "europej", "pozost"]


def find_keywords(text):
    text = text.lower()
    founded = []
    for keyword in keywords:
        if keyword in text:
            founded.append(keyword)
    return founded


def open_article(url):
    req = requests.get(url)
    if req.status_code != 200:
        print("unable to open: " + url)
        return

    bs = BeautifulSoup(req.text, "html.parser")
    time = bs.find("time")
    mydivs = bs.findAll("article", {"class": "single-page-content"})
    text = ""
    for div in mydivs:
        text = text + "\n" + div.text
    return text, time.text


def main():
    for i in range(max_index):
        url = search_url + "page=" + str(i)
        req = requests.get(url)
        if req.status_code != 200:
            print("Unable to get: " + url)
            continue
        bs = BeautifulSoup(req.text, "html.parser")
        mydivs = bs.findAll("section", {"class": "news-block"})
        for div in mydivs:
            article_url = div.find("header").find("a")["href"]
            url = urljoin(base_url, article_url)
            text, time = open_article(url)
            result = find_keywords(text)
            if len(result) > 0:
                print(time, url, result)


if __name__ == "__main__":
    main()
