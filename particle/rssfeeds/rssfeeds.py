#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from thready import threaded
from datetime import datetime
from dateutil import parser
import json
import requests
import logging

# custom modules:
from particle.common import db, DEBUG
from particle.rssfeeds.article_extractor import extract_article
from particle.helpers import *

log = logging.getLogger('particle')

def parse_rss_date(entry):
  if entry.has_key('updated_parsed'):
    dt = entry['updated_parsed']
    return datetime(
        dt.tm_year, 
        dt.tm_mon, 
        dt.tm_mday, 
        dt.tm_hour, 
        dt.tm_min, 
        dt.tm_sec
      )
  elif entry.has_key('updated'):
    return parser.parse(entry('updated'))
  else:
    return None

def parse_one_entry(entry_arg_set):
  """
  parse an entry in an rss feed
  """
  entry, data_source, full_text, config = entry_arg_set

  # open url to get actual link
  if entry.has_key('link') and entry['link'] != '' and entry['link'] is not None:
    r = requests.get(entry['link'])
    if r.status_code == 200:
      # parse and sluggify url
      article_url = parse_url(r.url)
      article_slug = sluggify(article_url)

    else:
      article_url = None
      article_slug = None

    # check if this is a relevant article
    if is_article(article_url, config):
      
      # check if this key exists
      if not db.exists(article_slug + ":article"):

        # parse date
        dt = parse_rss_date(entry)
        if dt is not None:
          time_bucket = round_datetime(dt, config)
          raw_timestamp = int(dt.strftime('%s'))
          pub_date = dt.strftime('%Y-%m-%d %H:%M:%S')

        else:
          time_bucket = gen_time_bucket(config)
          raw_timestamp = current_timestamp(config)
          pub_date = None

        # parse_title
        if entry.has_key('title'):
          rss_title = entry['title']

        else:
          rss_title = None

        # parse content
        if entry.has_key('summary'):
          rss_content = strip_tags(entry['summary'])
          rss_html = entry['summary']
        else:
          rss_content = None

      # if feed is not full text, extract the article content
        # by crawling the page
        if not full_text:
          article_datum = extract_article(article_url, config)
          extracted_urls = extract_urls(article_datum['extracted_html'], config, False)
          extracted_imgs = extract_imgs(article_datum['extracted_html'])
        else:
          article_datum = {}
          extracted_urls = extract_urls(rss_html, config, False)
          extracted_imgs = extract_imgs(rss_html)

        # rss datum
        rss_datum = dict(
          article_slug = article_slug,
          article_url = article_url,
          time_bucket = time_bucket,
          raw_timestamp = raw_timestamp,
          rss_pub_date = pub_date,
          rss_raw_link = r.url,
          rss_title = rss_title,
          rss_content = rss_content,
          rss_html = rss_html,
          extracted_urls = extracted_urls,
          extracted_imgs = extracted_imgs
        )
        
        # merge data
        complete_datum = dict(
          rss_datum.items() + 
          article_datum.items()
        )

        value = json.dumps({data_source: complete_datum})
        log.info( "RSSFEEDS\tNew post on %s\t%s" % (data_source, article_url) )
        
        # upsert the data
        upsert_rss_pub(article_url, article_slug, value)
  

def parse_one_feed(feed_arg_set):
  feed_url, data_source, full_text, config = feed_arg_set
  """
  parse all the items in an rss feed
  """
  
  feed_data = feedparser.parse(feed_url)
  
  entries = feed_data['entries']
  entry_arg_sets = [(entry, data_source, full_text, config) for entry in entries]

  threaded_or_serial(entry_arg_sets, parse_one_entry, 30, 100)

def run(config):
  """
  parse all teh feedz
  """
  # generate args from config
  if not isinstance(config['rssfeeds'], dict):
    raise ParticleConfigException("""'rssfeeds' field must be a set of key/value pairs.

      """)

  feed_arg_sets = []
  for data_source, v in config['rssfeeds'].iteritems():
    if not v.has_key('full_text'):
      v['full_text'] = False
    feed_arg = (v['feed_url'], data_source, v['full_text'], config)
    feed_arg_sets.append(feed_arg)

  # thread that shit!
  threaded_or_serial(feed_arg_sets, parse_one_feed, 5, 100)
