#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 抓大盤日成交量
# By Toomore
from datetime import datetime, timedelta
import urllib2, logging, csv, re
 
class ggm(object):
 
  def __init__(self,year,savef):
    starttime = 0
    daterange = datetime.today()
    f = open('%s.csv' % savef,'wt')
    writer = csv.writer(f)
    while 1:
      if daterange.year <= year:
        break
      else:
        daterange = datetime.today() - timedelta(days = 30 * starttime)
        for i in self.fetch_data(daterange):
          if self.ckinv(i):
            ti = []
            for ii in range(len(i)):
              i[ii] = i[ii].replace(',','')
              i[ii] = i[ii].replace(' ','')
              ti.append(i[ii])
            print ti
            writer.writerow(tuple(ti))
        starttime += 1
    f.close()
 
  def fetch_data(self, nowdatetime):
    """ Fetch data from twse.com.tw
        return list.
    """
    url = "http://www.twse.com.tw/ch/trading/exchange/FMTQIK/FMTQIK2.php?STK_NO=&myear=%(year)d&mmon=%(mon)02d&type=csv" % {'year': nowdatetime.year, 'mon': nowdatetime.month}
    logging.info(url)
    cc = urllib2.urlopen(url)
    #print cc.info().headers
    csv_read = csv.reader(cc)
    return csv_read
 
  def ckinv(self,oo):
    """ check the value is date or not """
    pattern = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{2}")
    b = re.search(pattern, oo[0])
    try:
      b.group()
      return True
    except:
      return False
