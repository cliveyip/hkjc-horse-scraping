

import scrapy


class ResultSpider(scrapy.Spider):
    name = "result"

    def start_requests(self):
        urls = [
            'http://racing.hkjc.com/racing/info/meeting/Results/english/Local/20170125/HV/',
            'http://racing.hkjc.com/racing/info/meeting/Results/english/Local/20170125/HV/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        yield {
            'page': response.url.split("/")[-2],
            # race-meeting has a lot of white-space TODO remove before outputting
            'race-meeting': response.css('.color_black::text').extract(),
            'class': response.css('.divWidth::text').extract(),
            'distance': response.css('.divWidth .number14::text').extract(),
            'going': response.css('.raceinfoDivWidth+ td::text').extract(),
            'track-type': response.css('.tableBorder0.font13 tr:nth-child(2) td:nth-child(1)::text').extract(),
            'course-type': response.css('.tableBorder0 tr:nth-child(2) td~ td+ td::text').extract(),
            'horse': response.css('.fontStyle:nth-child(3) a::text').extract(),
            'jockey': response.css('.fontStyle:nth-child(4) a::text').extract(),
            'trainer': response.css('.fontStyle~ .fontStyle+ .fontStyle a::text').extract(),
            # plc (#place) has problems - grabs running pos as well - workaround: just use ascending order
            # 'plc': response.css('thead+ tbody td:nth-child(1)::text').extract(),
            'draw': response.css('tbody td:nth-child(8)::text').extract(),
            'LBW': response.css('tbody td:nth-child(9)::text').extract(),
            'win-odds': response.css('tbody td:nth-child(12)::text').extract(),
        }
