from django.utils.text import slugify
from source.browser import Browser
from datetime import datetime
from .logger import Log
import uuid, re

class BurburinhoNews(Browser):
    def __init__(self, log: Log):
        super(BurburinhoNews, self).__init__(log)
        self.log = log
        self.url = "https://burburinhonews.com.br/categorias/noticias/page/"
        self.pxpath = dict(
            title = '//article/div/h2/a[@class="post-url post-title"]',
            link = '//article/div/h2/a[@class="post-url post-title"]',
            date = '//article/div/div/span/time',
        )
        self.sxpath = dict(
            text = '//div[@class="entry-content clearfix single-post-content"]',
            tag = '//a[@rel="tag"]',
            category = '//div[@class="post-header-title"]/div[@class="term-badges floated"]/span'
        )
        self.per_page = 10

    async def page(self, url):
        tree = await super().page(url, self.log)
        self.log.msg.debug(f"Page fetched from {url}")
        return data_page(self, tree)
    
    async def posts(self, news_on_page, model):
        self.log.msg.debug(f"Processing posts")
        await super().posts(news_on_page, model, self.sxpath, self.log)

class BahiaNoAr(Browser):
    def __init__(self, log: Log):
        super(BahiaNoAr, self).__init__(log)
        self.log = log
        self.url = "https://bahianoar.com/categoria/noticias/page/"
        self.pxpath = dict(
            title = '//div[@class="row mb-4"]/div/a/p',
            link = '//div[@class="row mb-4"]/div/a',
            date = '//div[@class="row mb-4"]/div/a/div[@class="debug-date d-flex align-items-center font-weight-normal mb-1"]/p',
        )
        self.sxpath = dict(
            text = '//div[@class="post-content"]',
            tag = '//div[@class="post_tags d-inline-block"]/a',
            category = '//a[@rel="category tag"]'
        )
        self.per_page = 10

    async def page(self, url):
        tree = await super().page(url, self.log)
        self.log.msg.debug(f"Page fetched from {url}")
        return data_page(self, tree)
    
    async def posts(self, news_on_page, model):
        self.log.msg.debug(f"Processing posts")
        await super().posts(news_on_page, model, self.sxpath, self.log)

class JornalGrandeBahia(Browser):
    def __init__(self, log: Log):
        super(JornalGrandeBahia, self).__init__(log)
        self.log = log
        self.url = "https://jornalgrandebahia.com.br/ultimas-noticias/page/"
        self.pxpath = dict(
            title = '//header[@class="mh-posts-list-header"]/h3[@class="entry-title mh-posts-list-title"]/a',
            link = '//header[@class="mh-posts-list-header"]/h3[@class="entry-title mh-posts-list-title"]/a',
            date = '//span[@class="entry-meta-date updated"]/a',
        )
        self.sxpath = dict(
            text = '//div[@class="entry-content clearfix"]',
            tag = '//a[@rel="tag"]',
            category = '//header/div/span/a[@rel="category tag"]',
        )
        self.per_page = 25

    async def page(self, url):
        tree = await super().page(url, self.log)
        self.log.msg.debug(f"Page fetched from {url}")
        return data_page(self, tree)
    
    async def posts(self, news_on_page, model):
        self.log.msg.debug(f"Processing posts")
        await super().posts(news_on_page, model, self.sxpath, self.log)

class LfNews(Browser):
    def __init__(self, log: Log):
        super(LfNews, self).__init__(log)
        self.log = log
        self.url = "https://lfnews.com.br/categorias/noticias/page/"
        self.pxpath = dict(
            title = '//div[@class="entry-blog-header"]/h2',
            link = '//div[@class="entry-blog-header"]/h2/a',
            date = '//span[@class="post-meta-date"]'
        )
        self.sxpath = dict(
            text = "//div[@class='post-body clearfix']",
            tag = '//a[@rel="tag"]',
            category = '//a[@class="post-cat"]'
        )
        self.per_page = 10
    
    async def page(self, url):
        tree = await super().page(url, self.log)
        self.log.msg.debug(f"Page fetched from {url}")
        return data_page(self, tree)
    
    async def posts(self, news_on_page, model):
        self.log.msg.debug(f"Processing posts")
        await super().posts(news_on_page, model, self.sxpath, self.log)

class RelataBahia(Browser):
    def __init__(self, log: Log):
        super().__init__(log)
        self.log = log
        self.url = "https://relatabahia.com.br/noticias/pagina/"
        self.pxpath = dict(
            title = '//div[@class="box_titulo"]',
            link = '//div[@class="box_titulo"]/h4/a',
            date = '//div[@class="data_horizontal"]',
        )
        self.sxpath = dict(
            text = '//div[@class="conteudo_post"]',
            tag = '//div[@class="lista_tags_noticias"]/ul/li',
            category = '//h2[@class="nome_categoria"]'
        )
        self.per_page = 30

    async def page(self, url):
        tree = await super().page(url, self.log)
        self.log.msg.debug(f"Page fetched from {url}")
        return data_page(self, tree)
    
    async def posts(self, news_on_page, model):
        self.log.msg.debug(f"Processing posts")
        await super().posts(news_on_page, model, self.sxpath, self.log)
    
class VilasMagazine(Browser):
    def __init__(self, log: Log):
        super(VilasMagazine, self).__init__(log)
        self.log = log
        self.url = "https://vilasmagazine.com.br/categoria/noticias/page/"
        self.pxpath = dict(
                title = '//div[@class="td-module-container td-category-pos-image"]/div[@class="td-module-meta-debug"]/h3[@class="entry-title td-module-title"]/a',
                link = '//div[@class="td-module-container td-category-pos-image"]/div[@class="td-module-meta-debug"]/h3[@class="entry-title td-module-title"]/a',
                date = '//div[@class="td_block_inner tdb-block-inner td-fix-index"]/div/div[@class="td-module-container td-category-pos-image"]/div[@class="td-module-meta-debug"]/div[@class="td-editor-date"]/span[@class="td-author-date"]/span[@class="td-post-date"]/time[@class="entry-date updated td-module-date"]',
        )
        self.sxpath = dict(
            text = '//div[@class="td-post-content tagdiv-type"]',
            tag = '//ul[@class="td-tags td-post-small-box clearfix"]/li/a',
            category = '//ul[@class="td-category"]/li/a'
        )
        self.per_page = 12
    
    async def page(self, url):
        tree = await super().page(url, self.log)
        self.log.msg.debug(f"Page fetched from {url}")
        return data_page(self, tree)
    
    async def posts(self, news_on_page, model):
        self.log.msg.debug(f"Processing posts")
        await super().posts(news_on_page, model, self.sxpath, self.log)

def data_page(self, tree):
    elements = dict()
    elements.update({
        xpath: tree.xpath(self.pxpath[xpath])
        for xpath in self.pxpath
    })

    if len(elements["title"]) != 0:
        elements_treaties = zip(
            [slugify(f"{get_slug(element.get('href'))}_{uuid.uuid4().hex[:8]}")
             for key, element in enumerate(elements['link'])],
            [str(element.text_content()).strip() for element in elements["title"]],
            [element.get("href") for element in elements["link"]],
            [datetime.strptime(date_format(element.text_content().strip()), "%d/%m/%Y").date() 
             for element in elements['date']]
        )
        return tuple(elements_treaties)
    else: return None

def date_format(date):
    date = re.sub(r'[\r\n]+', ' ', date)
    date = re.sub(r'\s+', ' ', date)
    date = date.strip()
    
    mouths = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    if "/" not in str(date):
        date = date.split(" ")
        if len(date) == 3:
            mouth = date[1].lower().replace(",", "")
            mouth = mouth[:3]
            index = mouths.index(mouth)+1
            if len(str(date[0])) == 1:
                date[0] = f'0{date[0]}'
            if len(str(index)) == 1:
                return f"{date[0]}/0{index}/{date[-1]}"
            return f"{date[0]}/{index}/{date[-1]}"
        elif len(date) == 5:
            mouth = date[2].lower()
            mouth = mouth[:3]
            index = mouths.index(mouth)+1
            if len(str(date[0])) == 1:
                date[0] = f'0{date[0]}'
            if len(str(index)) == 1:
                return f"{date[0]}/0{index}/{date[-1]}"
            return f"{date[0]}/{index}/{date[-1]}"
    elif "h" in date:
        date = date.split(" ") 
        return date[-2]
    else:
        return date

def get_slug(url):
    url = url.split('/')
    if url[-1] != "":
        return url[-1]
    else:
        return url[-2]
