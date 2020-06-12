import scrapy, re
from scrapy import Request
from indeedspider.items import IndeedspiderItem
from datetime import datetime, timedelta


class IndeedSpider(scrapy.Spider):
    name = 'indeedbot'
    
    def __init__(self, *args, **kwargs):
        super(IndeedSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')


    def start_requests(self):
        start_urls = self.start_urls
        for url in start_urls:
            yield Request(url, callback=self.parse)
            
    def parse(self,response):
        # Grab page items link
        next_page = response.xpath('//link[@rel="next"]/@href').extract()
        page_urls = response.xpath('//a[@class="jobtitle turnstileLink "]/@href').extract()
        for page_url in page_urls:
            yield Request(response.urljoin(page_url), callback = self.parse_page)
        # check if Next page link is available
        next_page = response.xpath('//link[@rel="next"]/@href').extract()
        if next_page:
            yield Request(response.urljoin(''.join(next_page)), callback = self.parse)
    
    def parse_page(self,response):
        MONTHS = ['Jan', 'Fev', 'Mar', 'Apr','May', 'Jun', 'Jul', 'Sep', 'Oct', 'Nov', 'Dec']
        JOB_TYPES = ['full-time', 'contract','part-time','temporary','intership','permanent', 'full time']
        hiring_organization = response.xpath('//div[@class="jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating"]/div//text()').extract()[0]
        job_title =  response.xpath('//div[contains(@class,"jobsearch-JobInfoHeader-title")]/h3/text()').extract() 
        # Extracting Job type
        job_description_data1= response.xpath('//*[contains(@class,"jobsearch-JobMetadataHeader")]/text()').extract()
        employement_type1 = [x for x in JOB_TYPES if x in ",".join(job_description_data1).lower()]
        job_description_data2 = response.xpath('//div[@class="jobsearch-jobDescriptionText"]').extract()
        employement_type2 = [x for x in JOB_TYPES if x in ",".join(job_description_data2).lower()]
        if employement_type1:
            employement_type = employement_type1
        elif employement_type2:
            employement_type = employement_type2
        else:
            employement_type = 'n.a'
        base_salary1 = re.findall('\$(.*?) .',str(response.xpath('//div[@class="jobsearch-JobMetadataHeader-item "]').extract()))
        base_salary2 = re.findall('\$(.*?) .',str(response.xpath('//*[@class="jobsearch-JobMetadataHeader-iconLabel"]/text()').extract()))
        if base_salary1:
            base_salary = base_salary1
        else:
            base_salary = base_salary2
        date_posted = re.findall('\d+',''.join([x for x in response.xpath('//div[@class="jobsearch-JobMetadataFooter"]//text()').extract() if 'day' in x ]))
        if date_posted:
            date_posted = datetime.now() - timedelta(days=int(date_posted[0]))
            date_posted = date_posted.strftime("%d/%m/%Y")
        else:
            date_posted = datetime.now().strftime("%d/%m/%Y")
        valid_through = re.findall('Posting End Date: (.+)',''.join(job_description_data2))
        job_posting_url = response.url
        
        items = IndeedspiderItem(
            hiring_organization = hiring_organization,
            job_title = job_title,
            employment_type = employement_type,
            base_salary = base_salary,
            date_posted = date_posted,
            valid_through = valid_through,
            job_posting_url = job_posting_url
        ) 
        yield items
    