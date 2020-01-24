import requests  #importing this to get html pages with all meta
from lxml import html  #importing that to parse html pages, includes cssselect, which helps us to navigate by CSS-markdown


class Crawling:
    def __init__(self):
        self.plain = dict()
        self.outplayed = []

    def get_data(self):
        for v in self.plain.values(): #looping through dict with node-pages and articles' links within
            for article in v:  #looping through articles' links
                raw_article = html.document_fromstring((requests.get(article, allow_redirects=False)).content) #getting full html page
                self.outplayed.append([{article: ' '.join(i.text_content() for i in raw_article.cssselect("[class=entry-content] p"))},# adding arcticle content
                                 {'time': (raw_article.cssselect("[class=posted-on] time"))[0].text_content()},  #time
                                 {'author': (raw_article.cssselect("[class=byline] a"))[0].text_content()}])  #author to list, according to .json file formatting

    def output(self):
        import json  #this will bring some structure to our data
        with open('data.json', 'w', 4, 'utf-8') as fp:  #writing data to .json file
            json.dump(self.outplayed, fp, skipkeys=False, ensure_ascii=False)

    def snatch_urls(self, url, rng): #the function takes node-url as the first argument and the number of node-pages to generate
        urls = []
        url_tree = dict()
        for i in range(1, rng):  #genering node-pages
            urls.append(url.replace(url[-1], str(i)))

        for link in urls:  #getting md for data
            url_tree[link] = requests.get(link, allow_redirects=True).content

        for k, v in url_tree.items():  #getting full html
            self.plain[k] = v.content

        for ke, ve in self.plain.items():
            try:
                self.plain[ke] = html.document_fromstring(ve)

            except ValueError:
                return 0

        for key, value in self.plain.items():  #snatching links from node-pages
            self.plain[key] = [i.get('href') for i in value.cssselect("[class=entry-title] a")]


crawl = Crawling()  #claiming a class method
crawl.snatch_urls("https://panorama.pub/category/news/society/page/1", 10)
crawl.get_data()
crawl.output()
