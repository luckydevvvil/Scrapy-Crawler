# -*- coding: utf-8 -*-
import scrapy
import sys  

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from hh.items import HhItem

reload(sys)
sys.setdefaultencoding('utf8')

class LabourSpider(CrawlSpider):
	name = "labour"
	allowed_domains = ["www.hh.ru", "hh.ru", "http://hh.ru/"]
	
	start_urls = [
		'https://ufa.hh.ru/vacancies/programmist',
		'https://ufa.hh.ru/vacancies/bukhgalter',
		'https://ufa.hh.ru/vacancies/inzhener',
		'https://ufa.hh.ru/vacancies/menedzher_po_prodazham',
		'https://ufa.hh.ru/vacancies/direktor',
		'https://ufa.hh.ru/vacancies/administrator',
		'https://ufa.hh.ru/vacancies/marketolog',
		'https://ufa.hh.ru/vacancies/dizayner',
		'https://ufa.hh.ru/vacancies/yurist'
	]

	def parse(self, response):
		
		SET_SELECTOR = 'div.search-result-description'
		
		for brickset in response.css(SET_SELECTOR):
			
			NAME_SELECTOR = 'a ::text'
			SALARY_SELECTOR = 'div.b-vacancy-list-salary ::text'
			COMPANY_SELECTOR = 'a ::text'

			if 'programmist' in response.url:
				specialty = 'Программист'
			if 'bukhgalter' in response.url:
				specialty = 'Бухгалтер'
			if 'inzhener' in response.url:
				specialty = 'Инженер'
			if 'menedzher_po_prodazham' in response.url:
				specialty = 'Менеджер по продажам'
			if 'direktor' in response.url:
				specialty = 'Директор'
			if 'administrator' in response.url:
				specialty = 'Администратор'
			if 'marketolog' in response.url:
				specialty = 'Маркетолог'
			if 'dizayner' in response.url:
				specialty = 'Дизайнер'
			if 'yurist' in response.url:
				specialty = 'Юрист'
						
			yield {
				'Заголовок': brickset.css(NAME_SELECTOR).extract_first(),
				'Зарплата': brickset.css(SALARY_SELECTOR).extract_first(),
				'Компания': brickset.css(COMPANY_SELECTOR).extract()[1],
				'Специальность': specialty
			}
			
		NEXT_PAGE_SELECTOR = 'div.b-pager__arrows > .b-pager__next a ::attr(href)'
		next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()

		if next_page:
			yield scrapy.Request(
                response.urljoin(next_page),
                callback = self.parse
			)

