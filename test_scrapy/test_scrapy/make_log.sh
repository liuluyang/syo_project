#!/bin/bash


t=$(date -d today +"%Y-%m-%d_%T")

mv /root/test_scrapy/test_scrapy/test_scrapy/test_scrapy.log  /root/test_scrapy/test_scrapy/test_scrapy/logs/"${t}".log