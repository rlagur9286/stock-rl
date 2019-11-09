import FinanceDataReader as fdr
import pandas as pd
import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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

