import requests
from bs4 import BeautifulSoup
# import pandas as pd

from assets.database import db_session
from assets.models import Data

import datetime

def get_kabuka_info():
    url = 'https://stocks.finance.yahoo.co.jp/stocks/detail/?code=7953.T'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    name = soup.select('.symbol')[0].string

    ka = soup.select('dd[class="ymuiEditLink mar0"] strong')
    kabu = []
    for k in ka:
        kabu.append(k)

    kabuka = int(kabu[1].string)
    dekidaka = kabu[4].string
    dekidaka = int(dekidaka.replace(',', ''))

    results = {
        'name' : name,
        'kabuka' : kabuka,
        'dekidaka' : dekidaka
    }

    return results

def w_data():

    _results = get_kabuka_info()

    date = datetime.date.today()
    kabukas = _results['kabuka']
    dekidakas = _results['dekidaka']

    row = Data(date = date, kabukas = kabukas, dekidakas = dekidakas)

    db_session.add(row)
    db_session.commit()

if __name__ == "__main__":
    w_data()
