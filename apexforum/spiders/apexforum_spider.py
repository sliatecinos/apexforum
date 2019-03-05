# -*- coding: utf-8 -*-
# #Spider de crawling dos fóruns no site do game Apex Legends

import scrapy
from .fld import FLD as flt
from bs4 import BeautifulSoup
from scrapy.http.request import Request
from scrapy import Selector

class ApexforumSpider(scrapy.Spider):
    name = "apexforum"

    def __init__(self):
        # Incluir a url inicial de pesquisa dos fóruns na página:
        # https://answers.ea.com/t5/Apex-Legends/ct-p/apex-legends-pt
        url = [
            'https://answers.ea.com/t5/Informacoes-de-jogos/Saudacoes-legends-Bem-vindos-a-comunidade-Apex/td-p/7443637',
        ]
        urlsappend = "/jump-to/first-unread-message/"
        self.start_urls = [x + urlsappend for x in url]
        self.log(["===== Página pesquisada -> %s =======" % urllog for urllog in self.start_urls])

    def parse(self, response):
        """
        Função de identificação de conteúdo das postagens nas páginas do Fórum APEX Legends
        """
        # Variaveis de captura dos dados de interesse nas páginas do Fórum
        page = response.url
        title = response.css("h1.ahq-board-title.D3 span::text").get()
        post = response.xpath('.//div[contains(@class, "lia-message-body")]//div[@class="lia-message-body-content"]').extract()
        username = response.xpath('//a[@class="lia-link-navigation lia-page-link lia-user-name-link"]//span//text()').extract()
        kudos = response.css("span.MessageKudosCount.lia-component-kudos-widget-message-kudos-count::text").getall()
        postdate = response.xpath('//span[@class="DateTime lia-message-posted-on lia-component-common-widget-date"]//span//@title').getall()
        next_topic = response.xpath('//li[@class="lia-paging-page-next lia-component-next"]//a[@class="lia-link-navigation"]//@href').get()
        next_page = response.xpath('//li[@class="lia-paging-page-next lia-component-next"]//a[@aria-label="Próxima página"]//@href').get()

        # Funçao "build-in" decode para interpretação dos caracteres utf-8
        # e funções de limpeza de caracteres não-interpretáveis
        result_title = flt.unescapeStr(title)
        result_title = bytes(result_title, "utf16").decode("utf16")
        result_title = flt.unescapeXml(result_title)

        result_kudos = [int(i.strip()) for i in kudos]

        # BeautifulSoup para "limpar" tags html de cada post na <lista>: post
        soup = [BeautifulSoup(i, features="lxml") for i in post]

        # Funçao build-in idem "title" e limpeza dos chars não-imprimíveis
        result_post = [(i.get_text()).strip() for i in soup]
        result_post = [flt.unescapeStr(i) for i in result_post]
        result_post = [bytes(i, "utf16", 'ignore').decode("utf16") for i in result_post]
        final_post = [flt.unescapeXml(i) for i in result_post]

        # Limpeza das datas dos posts
        result_date = [i.encode("ascii", 'ignore').decode("ascii") for i in postdate]

        # Captura do tópico dos posts
        topic = [page.split("/")[4]] * len(result_post)

        # Output das variáveis com os dados
        for apex in range(len(final_post)):
            yield {
                'forum_url': page,
                'forum_topic': topic[apex],
                'forum_title': result_title.strip(),
                'forum_post_date': result_date[apex],
                'forum_kudos': result_kudos[apex],
                'forum_user':  username[apex],
                'forum_posts': final_post[apex],
            }
        # Loop para paginação do mesmo tópico, em seguida vai para o próximo
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        elif next_topic is not None:
            yield response.follow(next_topic, callback=self.parse)
