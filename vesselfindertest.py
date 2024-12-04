from urllib.request import urlopen
import requests
import time
import pandas as pd
from database_storage import saveVesselstoDB

def main_scraper():
    #this is the url of PCT
    url = "https://www.pct.com.gr/vessels/longtermscheduled"
    page = requests.get(url, verify=True)
    html = page.text

    #lets find the spot of the page count, the pager
    pager_index = html.find('<ul class="pager__items js-pager__items">')
    #this is where it ends
    pager_end = html.find('</ul>', pager_index)

    pager_text=html[pager_index:pager_end]
    #if I count the list items (li) I shall know how many pages
    no_of_pages=pager_text.count('<li')
    tables=[] # this is where I shall keep each page

    urls=[]
    urls.append('https://www.pct.com.gr/vessels/longtermscheduled')
    #this is a loop that will create the urls for each page
    for i in range(no_of_pages-2):
        urls.append("https://www.pct.com.gr/vessels/longtermscheduled?page={}".format(i+1))

    for thisurl in urls:
        #sleep for 2 seconds to avoid being blocked as attacker
        time.sleep(2)
        page = urlopen(thisurl)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        table_MN = pd.read_html(html)
        tables.append(table_MN[0])
    #this dataframe contains all data from the page
    df=pd.concat(tables)

    #I get the unique vessel names, filtering by CMA operated
    cmavessels=df[df['Vessel Operator']=='CMA']['Vessel Name  Sort descending'].unique().copy()
    #this is the list, joined for use with SQL database
    vessellist=','.join(f'("{w}")' for w in cmavessels)
    saveVesselstoDB(vessellist)

def getTotalMoves(vesselname):
    import datetime
    import numpy as np
    d = {'key': vesselname, 'op': 'View', 'form_id':'vessels_search_form'}
    response=requests.post("https://www.pct.com.gr/vessels/scheduled/", data=d, verify=False)
    table_MN = pd.read_html(response.text)
    table1=table_MN[0].copy()
    today = datetime.date.today()
    table1['ddiff']=0
    table1['ddiff']=((pd.to_datetime(table1['etb'], format='%d/%m/%Y %H:%M').dt.date-today)/np.timedelta64(1, 'D')).astype(int).abs()
    voyage=table1.query('ddiff == ddiff.min()')['In Voyage'].iloc[0]
    moves=table1.query('ddiff == ddiff.min()')['est_moves'].iloc[0]
    return voyage,moves
