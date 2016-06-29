#!/usr/bin/env python

import sys
import re
import requests
import time
from dateutil.parser import parse
import datetime

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

def parse_page(html):
  # look for <th>Versions</th><td>...</td>
  ths = parse_ths(html)
  vers_td = ths['Versions']
  version = match("<strong>(.*?)<.strong>", vers_td)
  when = match("(\S+\s+\S+\s+\d+\s+\d+:\d+:\d+\s+\S+\s+\d+)", ths['Uploaded'])
  status = text_content(ths['Status'])

  t = parse(when)
  t = t.replace(tzinfo = None)

  return (version, t, status)

def scrape_doc_status(pkg):
  """Return the version, upload time and doc status string for a package."""
  url = "http://hackage.haskell.org/package/" + pkg
  r = requests.get(url)
  return parse_page(r.text)

