#!/usr/bin/python

### fetch google finance historical data ##

import httplib
import urllib2
import re


def debug_print( s, msg = None):
        print "DEBUG", msg, s
        pass

#  get url
# https://www.google.com/finance/historical?q=TPE:2330&startdate=1/31/1986&start=30&num=30

def get_site( stkID = 2330, month = 1, day = 1, year = 1985, start = 0, num =
30):
        return 'https://www.google.com/finance/historical?q=TPE:' + \
                str( stkID ) + '&startdate=' + \
                str(day) + '/' + str(month) + '/' + str(year) + \
               '&start=' + str(start) + '&num=' + str(num)
# testing
#debug_print(get_site(2485, 1, 31, 1986, 0, 200))
#debug_print(get_site())

# target source:
# date, open, high, low, close, volume
#<td class="lm">Jun 8, 2012
#<td class="rgt">77.00
#<td class="rgt">78.70
#<td class="rgt">77.00
#<td class="rgt">77.90
#<td class="rgt rm">34,628,000

pattern = r'<td class="lm">(.+)' +  \
           '\s<td class="rgt">([\d\.]+)' + \
           '\s<td class="rgt">([\d\.]+)' + \
           '\s<td class="rgt">([\d\.]+)' + \
           '\s<td class="rgt">([\d\.]+)' + \
           '\s<td class="rgt rm">([\d\,]+)'
reg_price = re.compile( pattern )

pattern_total_size =
r'google\.finance\.applyPagination\(\s+\d+,\s+\d+,\s+(\d+),\s+'
reg_row_size =  re.compile( pattern_total_size )

def write_fetch_data(fileName, stock_id = 0):
    f = open( fileName, 'a')
    if stock_id < 1000 :
        return None
    # Get web page content
    urlsite = get_site(stock_id, 1, 31, 1986, 0, 200)
    content = opener.open( urlsite ).read()

    match_r_sz = reg_row_size.search( content )
    if (match_r_sz is None):
        print "stock_id: "+ str(stock_id) + " not found! "
        return None

    ## write ID SZ line
    row_size = int (match_r_sz.groups()[0])
    id_line = "*ID:" + str(stock_id) + " SZ: " + str(row_size)
    print id_line
    f.write(id_line)
    f.write('\n')

    ## page number , 200rows/page
    page_num = row_size/200 + 1;
    print "pages: " + str(page_num)
    page_range = range(page_num)

    for i in page_range:
        start_pos = i*200
        site = get_site(stock_id, 1, 31, 1986, start_pos, start_pos+200)
        cnt = opener.open( site ).read()
        stock_data = reg_price.findall( cnt )
        length = len(stock_data)
        if (length is 0 ):
            print "stock_id: "+ str(stock_id) + " not found! "
            return None
        else:
            for i in range(length):
                f.write(str(stock_data[i]))
                f.write("\n")



#### Main ####
fileName = 'stock.data'
f = open(fileName, 'w')
f.close()  ## rewrite data
httplib.HTTPConnection.debuglevel = 1
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#stock_ids = range(9999)
stock_ids = (1111, 2330, 2485)

print 'Start Fetch!'
for stock_id in stock_ids:  # fetch all

    write_fetch_data(fileName, stock_id)