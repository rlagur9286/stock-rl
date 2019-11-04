import requests
import traceback
import pandas as pd
import datetime
import os

from bs4 import BeautifulSoup


def get_stock_fundamental_info(code_list, str_datefrom="2018-01-01"):
    for code in code_list:
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        res = requests.get(url)
        res.encoding = 'utf-8'
        soap = BeautifulSoup(res.text, 'lxml')
        el_table_navi = soap.find("table", class_="Nnavi")
        el_td_last = el_table_navi.find("td", class_="pgRR")
        pg_last = el_td_last.a.get('href').rsplit('&')[1]
        pg_last = pg_last.split('=')[1]
        pg_last = int(pg_last)

        if str_datefrom == "2018-01-01":
            str_datefrom = datetime.datetime.strftime(datetime.datetime(year=2018, month=1, day=1), '%Y.%m.%d')

        str_dateto = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')
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
        
        path_dir = 'data/{}-crawling'.format(datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d'))
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        path = os.path.join(path_dir, '{code}_{date_from}_{date_to}.csv'.format(code=code, date_from=str_datefrom, date_to=str_dateto))
        df.to_csv(path, index=False)

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

if __name__ == "__main__":
    # code = '035420'  # NAVER
    # code = '006800'  # 미래에셋대우
    # code = '005930'  # 삼성전자
    get_stock_fundamental_info(code_list=["035420", "006800", "005930"], str_datefrom="2018-01-01")