from dotenv import load_dotenv
import os

load_dotenv()

BOT_NAME = "course_radar"

SPIDER_MODULES = ["course_radar.spiders"]
NEWSPIDER_MODULE = "course_radar.spiders"

ROBOTSTXT_OBEY = True


ITEM_PIPELINES = {
   "course_radar.pipelines.MySQLPipeline": 1,
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# TODO: For testing purposes, before i implement pipeline to go to db or maybe use REDIS MQ?
FEEDS = {
    'output.json': {
        'format': 'json',
        'overwrite': True,
    },
}

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_DB = os.getenv('MYSQL_DB', 'my_db')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')

# Super important dont remove
DUPEFILTER_CLASS = "scrapy.dupefilters.BaseDupeFilter"