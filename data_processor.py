import requests
import traceback
import pandas as pd
import numpy as np
import datetime
import os
import re
import json
import FinanceDataReader as fdr

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from common.util import BASE_DIR

def get_stock_technical_info(code_list, str_datefrom="2018-01-01", save_date=None):
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
        
        # 크롤한 데이터 저장
        if not save_date:
            path_dir = os.path.join(BASE_DIR, 'data/{}-crawling/tech/'.format(datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')))
        else:
            path_dir = os.path.join(BASE_DIR, 'data/{}-crawling/tech/'.format(save_date))
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        path = os.path.join(path_dir, '{code}.csv'.format(code=code))
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

def get_stock_fundamental_info(code_list=[], save_date=None):
    try:
        browser  = Chrome("chromedriver")
        browser.maximize_window()
    except Exception as e:
        print("[ERROR] ", e)
        return []

    #code = 종목번호
    for code in code_list:
        base_url = 'https://finance.naver.com/item/coinfo.nhn?code='+ code + '&target=finsum_more'
        
        browser.get(base_url)
        #frmae구조 안에 필요한 데이터가 있기 때문에 해당 데이터를 수집하기 위해서는 frame구조에 들어가야한다.
        browser.switch_to_frame(browser.find_element_by_id('coinfo_cp'))
        
        #재무제표 "연간" 클릭하기
        browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[3]')[0].click()

        html0 = browser.page_source
        html1 = BeautifulSoup(html0,'html.parser')
        
        #기업명 뽑기
        title0 = html1.find('head').find('title').text
        
        html22 = html1.find('table',{'class':'gHead01 all-width','summary':'주요재무정보를 제공합니다.'})
        
        #date scrapy
        thead0 = html22.find('thead')
        tr0 = thead0.find_all('tr')[1]
        th0 = tr0.find_all('th')
        
        date = []
        for i in range(len(th0)):
            date.append(''.join(re.findall('[0-9/]',th0[i].text)))
        
        #columns scrapy
        tbody0 = html22.find('tbody')
        tr0 = tbody0.find_all('tr')
        
        col = []
        for i in range(len(tr0)):

            if '\xa0' in tr0[i].find('th').text:
                tx = re.sub('\xa0','',tr0[i].find('th').text)
            else:
                tx = tr0[i].find('th').text
            col.append(tx)
        
        #main text scrapy
        td = []
        for i in range(len(tr0)):
            td0 = tr0[i].find_all('td')
            td1 = []
            for j in range(len(td0)):
                if td0[j].text == '':
                    td1.append('0')
                else:
                    td1.append(td0[j].text)

            td.append(td1)
        
        td2 = list(map(list,zip(*td)))
        # 크롤한 데이터 저장
        if not save_date:
            path_dir = os.path.join(BASE_DIR, 'data/{}-crawling/fund/'.format(datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')))
        else:
            path_dir = os.path.join(BASE_DIR, 'data/{}-crawling/fund/'.format(save_date))
            
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        pd.DataFrame(td2, columns = col,index = date).to_csv(os.path.join(path_dir, "{code}.csv".format(code=code)), index=True, index_label="date")

def load_data(code_list, save_date):
    df = pd.DataFrame()
    for code in code_list:
        # Load fundermental info
        path_dir = os.path.join(BASE_DIR, 'data/{}-crawling/fund/'.format(save_date))
        if os.path.exists(os.path.join(path_dir, "{code}.csv".format(code=code))):
            print("Success to load fundmental #{code} stock info...".format(code=code))
            fund_df = pd.read_csv(os.path.join(path_dir, "{code}.csv".format(code=code)), index_col="date")
            fund_df['year'] = fund_df.index.tolist()
            fund_df['year'] = fund_df['year'].apply(lambda x: x.split("/")[0])

        # Load technical info
        path_dir = os.path.join(BASE_DIR, 'data/{}-crawling/tech/'.format(save_date))
        if os.path.exists(os.path.join(path_dir, "{code}.csv".format(code=code))):
            print("Success to load technical #{code} stock info...".format(code=code))
            tech_df = pd.read_csv(os.path.join(path_dir, "{code}.csv".format(code=code)), index_col="날짜")
            tech_df['year'] = tech_df.index.tolist()
            tech_df['year'] = tech_df['year'].apply(lambda x: x.split("/")[0])
            if not fund_df.empty:
                df_ = tech_df.merge(fund_df, on="year", how="left")
        else:
            print("Fail to load technical #{code} stock info...".format(code=code))
            continue
        df_['code'] = code
        df = pd.concat([df, df_])
    return df

def preprocess(data):
    prep_data = data
    windows = [5, 10, 20, 60, 120]
    for window in windows:
        prep_data['종가_ma{}'.format(window)] = prep_data['종가'].rolling(window).mean()
        prep_data['거래량_ma{}'.format(window)] = (prep_data['거래량'].rolling(window).mean())
    return prep_data

def build_training_data(prep_data):
    training_data = prep_data

    training_data['시가_last종가_비율'] = np.zeros(len(training_data))
    training_data.loc[1:, '시가_last종가_비율'] = (training_data['시가'][1:].values - training_data['종가'][:-1].values) / training_data['종가'][:-1].values
    training_data['고가_종가_비율'] = (training_data['고가'].values - training_data['종가'].values) / training_data['종가'].values
    training_data['저가_종가_비율'] = (training_data['저가'].values - training_data['종가'].values) / training_data['종가'].values
    training_data['종가_last종가_비율'] = np.zeros(len(training_data))
    training_data.loc[1:, '종가_last종가_비율'] = (training_data['종가'][1:].values - training_data['종가'][:-1].values) / training_data['종가'][:-1].values
    training_data['거래량_last거래량_비율'] = np.zeros(len(training_data))
    training_data.loc[1:, '거래량_last거래량_비율'] = (training_data['거래량'][1:].values - training_data['거래량'][:-1].values) / training_data['거래량'][:-1].replace(to_replace=0, method='ffill').replace(to_replace=0, method='bfill').values

    windows = [5, 10, 20, 60, 120]
    for window in windows:
        training_data['종가_ma%d_비율' % window] = \
            (training_data['종가'] - training_data['종가_ma%d' % window]) / \
            training_data['종가_ma%d' % window]
        training_data['거래량_ma%d_비율' % window] = \
            (training_data['거래량'] - training_data['거래량_ma%d' % window]) / \
            training_data['거래량_ma%d' % window]

    return training_data

def get_kosdaq_technical_info(code_list, str_datefrom="2018-01-01", save_date=None):

    # 한국거래소 상장종목 전체
    df_krx = fdr.StockListing('KRX')
    df_krx.head()

    df_krx = fdr.StockListing('KRX')
    target_lists = df_krx.loc[df_krx['Symbol'].isin(code_list)]

    if save_date is None:
        save_date = str(datetime.date.today())

    #res_df = pd.DataFrame()
    # LIST for 문 돌며 데이터 검색
    for idx, item in target_lists.iterrows():
        df = fdr.DataReader(item['Symbol'], str_datefrom, save_date)
        df['Stock_code'] = item['Symbol']
        df['Stock_name'] = item['Name']
        df['Stock_sector'] = item['Sector']

        # 크롤한 데이터 저장
        if not save_date:
            path_dir = os.path.join(BASE_DIR, 'data/{}-crawling/tech/'.format(
                datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')))
        else:
            path_dir = os.path.join(BASE_DIR, 'data/{}-crawling/tech/'.format(save_date))
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        path = os.path.join(path_dir, '{code}.csv'.format(code=item['Symbol']))
        df.to_csv(path, index=False)