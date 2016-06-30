#!/usr/bin/env python

import sys
import re
import requests
import time
from dateutil.parser import parse
import datetime
from collections import namedtuple

Package = namedtuple('Package', 'package version all_versions upload_time doc_status')

def warn(msg):
  sys.stderr.write(msg + "\n")

def parse_ths(html):
  ths = {}
  for m in re.finditer("<th>(.*?)</th>\s*<td>(.*?)</td>", html, re.S|re.M|re.I):
    ths[ m.group(1) ] = m.group(2)
  return ths

def match(pat, text):
  if text:
    m = re.search(pat, text)
    if m:
      return m.group(1)
  return ""

def text_content(html):
  return re.sub("<.*?>", " ", html)

def parse_page(html, pkg, url):
  if (not re.search('<table class="properties"', html)):
    return None
  # Returns a Package named tuple with parsed fields
  ths = parse_ths(html)
  if 'Versions' in ths:
    vers_td = ths['Versions']
    version = match("<strong>(.*?)<.strong>", vers_td)
    all_versions = [ v.group(0) for v in re.finditer('(\d[\d\.]+)', vers_td) ]
    # warn("=== vers_td: {}".format(vers_td))
  else:
    warn("url {} does not have section Versions".format(url))
    all_versions = []
    version = "unknown"

  if 'Uploaded' in ths:
    when = match("(\S+\s+\S+\s+\d+\s+\d+:\d+:\d+\s+\S+\s+\d+)", ths['Uploaded'])
  else:
    warn("url {} does not have section Uploaded".format(url))
    when = None
  
  if 'Status' in ths:
    status = text_content(ths['Status'])
  else:
    warn("url {} does not have section Status".format(url))
    status = ""

  t = parse(when)
  t = t.replace(tzinfo = None)

  return Package (package=pkg, all_versions=all_versions, version=version, upload_time=t, doc_status = status)

def scrape_doc_status(pkg, version = None):
  """Return the version, upload time and doc status string for a package."""
  if version:
    leaf = pkg + "-" + version
  else:
    leaf = pkg
  url = "http://hackage.haskell.org/package/" + leaf
  r = requests.get(url)
  p =  parse_page( r.text, pkg, url )
  return p

