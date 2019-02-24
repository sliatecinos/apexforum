# -*- coding: utf-8 -*-
##Spider de crawling dos fóruns no site do game Apex Legends
import scrapy
from .fld import FLD as flt
from bs4 import BeautifulSoup
from scrapy.http.request import Request


class ApexforumSpider(scrapy.Spider):
    name = "apexforum"

    def start_requests(self):
        # url inicial de pesquisa dos fóruns na página:
        # https://answers.ea.com/t5/Apex-Legends/ct-p/apex-legends-pt
        urlstart = [
            'https://answers.ea.com/t5/Problemas-tecnicos/APEX-Legends-fechando-sozinho/td-p/7499624',
            'https://answers.ea.com/t5/Problemas-tecnicos/Problemas-com-conetividade/td-p/7532786',
        ]
        urlsappend = ['/jump-to/first-unread-message']
        urls = [end + urlsappend.pop[0] for end in urlstart]

        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        """
        Função de identificação de conteúdo das postagens nas páginas do Fórum
        """
        # Variaveis de
        page = response.url
        title = response.css("h1.ahq-board-title.D3 span::text").get()
        div_p = response.xpath('//div[@class="lia-message-body-content"]').extract()
        username = response.xpath('//a[@class="lia-link-navigation lia-page-link lia-user-name-link"]//span//text()').extract()
        kudos = response.css("span.MessageKudosCount.lia-component-kudos-widget-message-kudos-count::text").getall()
        response.css("a.lia-link-navigation.lia-page-link.lia-user-name-link span::text").getall()
        xpathdate = response.xpath('//div[@class="lia-quilt-row lia-quilt-row-page_title_row"]//div//div//span[@class="header-created-by"]')
        postdate = xpathdate.xpath("//span/@title").extract()

        # BeautifulSoup para "limpar" tags html de cada post na <lista>: post
        soup = [BeautifulSoup(post, features="lxml") for post in div_p]

        # Função "build-in" decode para interpretação dos caracteres utf-8
        # e funções de limpeza de caracteres não-interpretáveis
        result_title = flt.unescapeStr(title)
        result_title = bytes(result_title, "iso-8859-1").decode("unicode_escape")
        result_title = flt.unescapeXml(result_title)

        result_kudos = [int(i.strip()) for i in kudos]
        # self.log(kudos[0].strip())
        # self.log(kudos[1].strip())
        # self.log(kudos[2].strip())

        result_post = [(i.get_text()).strip() for i in soup]
        result_post = [flt.unescapeStr(i) for i in result_post]
        result_post = [bytes(i, "iso-8859-1").decode("unicode_escape") for i in result_post]
        # final_post = [flt.unescapeXml(i) for i in result_post]

        for item in range(len(result_post)):
            yield {
                'url': page,
                'forum_user':  username[item],
                'forum_title': result_title.strip(),
                'forum_kudos_points': result_kudos[item],
                'forum_posts': result_post[item],
            }
