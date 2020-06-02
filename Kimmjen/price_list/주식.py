import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import os

code = '024110'

url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)

res = requests.get(url)
res.encoding = 'utf-8'
res.status_code

url

soap = BeautifulSoup(res.text, 'lxml')

el_table_navi = soap.find("table", class_="Nnavi")
el_td_last = el_table_navi.find("td", class_="pgRR")
pg_last = el_td_last.a.get('href').rsplit('&')[1]
pg_last = pg_last.split('=')[1]
pg_last = int(pg_last)
pg_last

def parse_page(code, page):
    try:
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table")), header=0)[0]
        _df = _df.dropna()
        return _df
    except Exception as e:
        traceback.print_exc()

    return None

parse_page(code, 1)

str_datefrom = datetime.datetime.strftime(datetime.datetime(year=2010, month=1, day=1), '%Y.%m.%d')
str_datefrom

str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')
str_dateto

df = None

for page in range(1, pg_last+1):
    _df = parse_page(code, page)
    _df_filtered = _df[_df['날짜'] > str_datefrom]
    if df is None:
        df = _df_filtered
    else:
        df = pd.concat([df, _df_filtered])
    if len(_df) > len(_df_filtered):
        break
df.tail()

path_dir = './price_data/'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)
path = os.path.join(path_dir, '{code}_{date_from}_{date_to}.csv'.format(code=code, date_from=str_datefrom, date_to=str_dateto))
path
df.to_csv(path, index=False)