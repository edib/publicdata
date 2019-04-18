# -*- coding: utf-8 -*-
import scrapy


class SecimSpider(scrapy.Spider):
    name = 'secim'
    allowed_domains = ['www.sozcu.com.tr']
    def start_requests(self):
        urls = []
        ilceler = ['adalar', 'arnavutkoy', 'atasehir', 'avcilar', 'bagcilar', 'bahcelievler', 'bakirkoy', 'basaksehir', 'bayrampasa', 'besiktas', 'beykoz', 'beylikduzu', 'beyoglu', 'buyukcekmece', 'catalca', 'cekmekoy', 'esenler', 'esenyurt', 'eyupsultan', 'fatih', 'gaziosmanpasa', 'gungoren', 'kadikoy', 'kagithane', 'kartal', 'kucukcekmece', 'maltepe', 'pendik', 'sancaktepe', 'sariyer', 'silivri', 'sultanbeyli', 'sultangazi', 'sile', 'sisli', 'tuzla', 'umraniye', 'uskudar', 'zeytinburnu']
        for i in ilceler:
            urls.append("https://www.sozcu.com.tr/secim2019/istanbul/"+i)
        filename = 'sonuc-%s.txt' % "istanbul"
        with open(filename, 'a') as f:
            f.write('"ilçe","kazanan parti","oy oranı","katilim oranı","kullanilan oy","geçerli oy","seçmen sayısı","geçersiz oy","geçersiz oranı"\n')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #self.logger.info('%s', response.xpath('/html/body/div[1]/div[4]/div/div/ul[1]/li[1]/span/text()').extract())
        main_xpath = '/html/body/div[1]/div[4]/div/div/ul[1]'
        kazanan = response.xpath('//*[@id="pgkbs"]/tbody/tr[1]/td[2]/a/text()').re(r'\w.*')[0]
        oy_oran = response.xpath('//*[@id="pgkbs"]/tbody/tr[1]/td[4]/text()').get()
        katilim = response.xpath('%s/li[1]/span/text()' % main_xpath).get()
        kullanilan = response.xpath('%s/li[2]/span/text()' % main_xpath).get().replace('.','')
        gecerli = response.xpath('%s/li[3]/span/text()' % main_xpath).get().replace('.','')
        toplam = response.xpath('%s/li[4]/span/text()' % main_xpath).get().replace('.','')
        gecersiz = int(kullanilan)-int(gecerli)
        gecersiz_oran = int(gecersiz)/int(kullanilan)*100.0
        ilce = response.url.split("/")[-1]
        filename = 'sonuc-%s.txt' % "istanbul"
        with open(filename, 'a') as f:
            f.write('"%s","%s","%s","%s","%s","%s","%s","%s","%.2f"\n'
            % (ilce,kazanan,oy_oran,katilim,
            kullanilan,
            gecerli,
            toplam,
            gecersiz, gecersiz_oran))
        #self.log('%s %s ' % (ilce,value))
