# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from collections import OrderedDict
import scrapy
import six


class OrderItems(scrapy.Item):
    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:
            for k, v in six.iteritems(dict(*args,**kwargs)):
                self[k] = v  
            

class IndeedspiderItem(OrderItems):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hiring_organization = scrapy.Field()
    job_title = scrapy.Field()
    employment_type = scrapy.Field()
    base_salary = scrapy.Field()
    date_posted= scrapy.Field()
    valid_through = scrapy.Field()
    job_posting_url = scrapy.Field()
    
