from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from lxml import html
import aiohttp, asyncio, re, requests, time
from source.logger import Log

class Browser(ABC):
    def __init__(self, log: Log):
        super().__init__()
        self.log = log

    @classmethod  
    @abstractmethod
    async def page(cls, url, log):
        async with aiohttp.ClientSession() as session:
            task = cls.fetch_page(session, url, log)
            html = await asyncio.gather(task)
            
        return html[0]

    @classmethod
    async def fetch_page(cls, session, url, log):
        while True:
            async with session.get(url) as response:
                if response.status == 429:
                    await asyncio.sleep(0.5)
                    log.msg.debug(f"Status: {response.status} | Url: {url}")
                else:
                    html_content = await response.text()
                    try:
                        html_content = re.sub(r'^<\?xml.*?\?>', '', html_content)
                    except Exception as e:
                        log.msg.error(f"Error: {str(e)}")
                        log.msg.debug(f"Msg: xml não encontrado")
                    soup = BeautifulSoup(html_content, 'html.parser')

                    return html.fromstring(soup.prettify())

    @classmethod  
    @abstractmethod
    async def posts(cls, news_on_page, model, xpath, log):
        models=['JornalGrandeBahia','LfNews','VilasMagazine','BurburinhoNews','BahiaNoAr','RelataBahia',]

        posts = dict()
        for data_post in news_on_page:
            posts.update({str(data_post[0]):{
                'slug': str(data_post[0]),
                'model': str(models.index(model)),
                'title': str(data_post[1]),
                'link': str(data_post[2]),
                'date': str(data_post[3]),
            }})
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for key in posts:
                if posts[key]['link'] != "https://bahianoar.com/gilberto-gil-reage-apos-xingamentos-em-jogo-da-copa-do-mundo-veja-video/":
                    tasks.append(cls.fetch_page(session, posts[key]['link'], log))
            htmls = await asyncio.gather(*tasks)
        try:
            for slug, tree in zip([posts[key]['slug'] for key in posts], htmls):
                exists = await cls.check_exists({"link": posts[slug]["link"]}, 'post')
                if exists == None:
                    await cls.posting(tree, posts[slug], xpath, log)
        except Exception as e:
            log.msg.error(f"Error processing posts: {e}")
        finally:
            log.msg.critical(f"Posts shaved")

    @classmethod
    async def check_exists(cls, data, object):
        if object == "post":
            url = 'http://127.0.0.1:8000/api/posts/check-exists/'
        if object == "tag":
            url = 'http://127.0.0.1:8000/api/tags/check-exists/'
        if object == "category":
            url = 'http://127.0.0.1:8000/api/categories/check-exists/'

        response = requests.post(url, json=data)
        resp = response.json()
        if resp["resp"] != None:
            return resp["resp"]
        else: return None
        
    @classmethod
    async def posting(cls, tree, post, xpath, log):
        headers = {'Content-Type': 'application/json'}
        for xph in xpath:
            temp = tree.xpath(xpath[xph])
            if xph == "text":
                post[xph] = temp[0].text_content().strip()
            if xph == "tag":
                try:
                    post["tags"] = list()
                    for tag in temp:
                        tag = await cls.get_slug(tag.get("href"))
                        data = {"tag": tag, "model": post["model"]}
                        exists = await cls.check_exists(data, 'tag')
                        if exists == None:
                            response = requests.post('http://127.0.0.1:8000/api/Tags/', json=data, headers=headers)
                            resp_data = response.json()
                            post["tags"].append(resp_data.get("id"))
                        else:
                            post["tags"].append(exists.get("id"))
                except Exception as e:
                    log.msg.error(f"Error processing posts: {e}")
                finally:
                   log.msg.info(f"All tags geted")
            if xph == "category":
                try:
                    post["categories"] = list()
                    for category in temp:
                        url_categ = tuple(category.get("href").split('/'))
                        for key, param in enumerate(url_categ):
                            if 'categ' in str(param):
                                url_categ = url_categ[key+1:-1]
                        for i in range(0, len(url_categ)):
                            if len(url_categ[i]) != 0:
                                data = {"category":url_categ[i], "model":post["model"]}
                                exists = await cls.check_exists(data, 'category')
                                if exists == None:
                                    response = requests.post('http://127.0.0.1:8000/api/Category/', json=data, headers=headers)
                                    resp_data = response.json()
                                    post["categories"].append(resp_data.get("id"))
                                else:
                                    post["categories"].append(exists.get("id"))
                except Exception as e:
                    log.msg.error(f"Error processing posts: {e}")
                finally:
                    log.msg.info(f"All categories geted")
        requests.post('http://127.0.0.1:8000/api/Post/', json=post, headers=headers)
        log.msg.info(f"post with slug {post['slug']} posted")
        
    @classmethod
    async def get_slug(cls, url):
        url = url.split('/')
        if url[-1] != "":
            return url[-1]
        else:
            return url[-2]
