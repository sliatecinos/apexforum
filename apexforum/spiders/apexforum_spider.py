# -*- coding: utf-8 -*-
## Spider de crawling dos fóruns no site do game Apex Legends

import scrapy
from .fld import FLD as flt
from bs4 import BeautifulSoup
from scrapy.http.request import Request
from scrapy import Selector


class ApexforumSpider(scrapy.Spider):
    name = "apexforum"

    def __init__(self):
        # url inicial de pesquisa dos fóruns na página:
        # https://answers.ea.com/t5/Apex-Legends/ct-p/apex-legends-pt
        url = [
            "https://answers.ea.com/t5/Problemas-tecnicos/NAO-E-POSSIVEL-SE-CONECTAR-AO-APEX-LEGENDS-ON-PC-21-02-2019/td-p/7537132",
        ]
        urlsappend = "/jump-to/first-unread-message/"
        self.start_urls = [x + urlsappend for x in url]
        self.log(["===== %s =======" % urllog for urllog in self.start_urls])

    def parse(self, response):
        """
        Função de identificação de conteúdo das postagens nas páginas do Fórum
        """
        # Variaveis de
        page = response.url
        title = response.css("h1.ahq-board-title.D3 span::text").get()
        post = response.xpath('//div[@class="lia-message-body-content"]').extract()
        username = response.xpath('//a[@class="lia-link-navigation lia-page-link lia-user-name-link"]//span//text()').extract()
        kudos = response.css("span.MessageKudosCount.lia-component-kudos-widget-message-kudos-count::text").getall()
        datepost = response.xpath('//span[@class="DateTime lia-message-posted-on lia-component-common-widget-date"]//span//@title').getall()
        next_topic = response.xpath('//li[@class="lia-paging-page-next lia-component-next"]//a[@class="lia-link-navigation"]//@href').get()
        next_page = response.xpath('//li[@class="lia-paging-page-next lia-component-next"]//a[@aria-label="Próxima página"]//@href').get()
        # idpost = response.xpath('//div[@class="lia-quilt-row lia-quilt-row-forum-title-row"]//div//div//div//div//div[0]').extract()

        # BeautifulSoup para "limpar" tags html de cada post na <lista>: post
        soup = [BeautifulSoup(i, features="lxml") for i in post]

        # Função "build-in" decode para interpretação dos caracteres utf-8
        # e funções de limpeza de caracteres não-interpretáveis
        result_title = flt.unescapeStr(title)
        result_title = bytes(result_title, "iso-8859-1").decode("unicode_escape")
        result_title = flt.unescapeXml(result_title)

        result_kudos = [int(i.strip()) for i in kudos]

        result_post = [(i.get_text()).strip() for i in soup]
        result_post = [flt.unescapeStr(i) for i in result_post]
        result_post = [bytes(i, "cp1252").decode("unicode_escape") for i in result_post]
        final_post = [flt.unescapeXml(i) for i in result_post]

        for apex in range(len(final_post)):
            yield {
                'url': page,
                'forum_title': result_title.strip(),
                'forum_posts': final_post[apex],
                'forum_user':  username[apex],
                'forum_kudos': result_kudos[apex],
                'forum_post_date': datepost[apex]
            }
                   
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
