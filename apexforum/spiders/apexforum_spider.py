# -*- coding: utf-8 -*-
## Spider de crawling dos fóruns no site do game Apex Legends

import scrapy
from .fld import FLD as flt
from bs4 import BeautifulSoup
from scrapy.http.request import Request
from scrapy import Selector

import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='apexforumlog.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class ApexforumSpider(scrapy.Spider):
    name = "apexforum"

    def __init__(self):
        # url inicial de pesquisa dos fóruns na página:
        # https://answers.ea.com/t5/Apex-Legends/ct-p/apex-legends-pt
        url = [
            "https://answers.ea.com/t5/Problemas-tecnicos/Possiveis-solucoes-para-crashes-erros-desconexoes-congelamento/m-p/7571666",
        ]
        urlsappend = "/jump-to/first-unread-message/"
        self.start_urls = [x + urlsappend for x in url]
        self.log(["===== Página Crawled-> %s =======" % urllog for urllog in self.start_urls])

    def parse(self, response):
        """
        Função de identificação de conteúdo das postagens nas páginas do Fórum APEX Legends
        """
        # Variaveis de captura dos dados de interesse nas páginas do Fórum
        page = response.url
        title = response.css("h1.ahq-board-title.D3 span::text").get()
        post = response.xpath('.//div[@class="lia-message-body lia-component-body"]//div[@class="lia-message-body-content"]').extract()
        username = response.xpath('//a[@class="lia-link-navigation lia-page-link lia-user-name-link"]//span//text()').extract()
        kudos = response.css("span.MessageKudosCount.lia-component-kudos-widget-message-kudos-count::text").getall()
        datepost = response.xpath('//span[@class="DateTime lia-message-posted-on lia-component-common-widget-date"]//span//@title').getall()
        next_topic = response.xpath('//li[@class="lia-paging-page-next lia-component-next"]//a[@class="lia-link-navigation"]//@href').get()
        next_page = response.xpath('//li[@class="lia-paging-page-next lia-component-next"]//a[@aria-label="Próxima página"]//@href').get()
        # idpost = response.xpath('//div[@class="lia-quilt-row lia-quilt-row-forum-title-row"]//div//div//div//div//div[0]').extract()

        # Função "build-in" decode para interpretação dos caracteres utf-8
        # e funções de limpeza de caracteres não-interpretáveis
        result_title = flt.unescapeStr(title)
        result_title = bytes(result_title, "iso-8859-1").decode("unicode_escape")
        result_title = flt.unescapeXml(result_title)

        result_kudos = [int(i.strip()) for i in kudos]


        # BeautifulSoup para "limpar" tags html de cada post na <lista>: post
        soup = [BeautifulSoup(i, features="lxml") for i in post]

        result_post = [(i.get_text()).strip() for i in soup]
        result_post = [flt.unescapeStr(i) for i in result_post]
        result_post = [bytes(i, "cp1252").decode("cp1252") for i in result_post]
        final_post = [flt.unescapeXml(i) for i in result_post]

        result_date = [i.encode("ascii",'ignore').decode("unicode_escape") for i in datepost]

        # Output das variáveis com os dados
        for apex in range(len(final_post)):
            yield {
                'forum_url': page,
                'forum_topic': page.split("/")[4],
                'forum_title': result_title.strip(),
                'forum_post_date': result_date[apex],
                'forum_kudos': result_kudos[apex],
                'forum_user':  username[apex],
                'forum_posts': final_post[apex],
            }
        # Loop para paginação do mesmo tópico, em seguida vai para o próximo
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        # elif next_topic is not None:
        #     yield response.follow(next_topic, callback=self.parse)
