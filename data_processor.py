from common.util import get_stock_technical_info
from common.util import get_stock_fundamental_info

from common.util_kosdaq import get_kosdaq_technical_info

from common.util import load_data

if __name__ == "__main__":
    # code = '035420'  # NAVER
    # code = '006800'  # 미래에셋대우
    # code = '005930'  # 삼성전자

    ###########################################
    # get stock info : KOSPI
    ###########################################
    # 기술적 분석 크롤링
    get_stock_technical_info(code_list=["035420", "006800", "005930"], str_datefrom="2018-01-01", save_date="2019-11-07")
    # 기본적 분석 크롤링
    get_stock_fundamental_info(code_list=["035420", "006800", "005930"], save_date="2019-11-07")

    ###########################################
    # get stock info : KOSDAQ
    ###########################################
    KOSDAQ_BIG = []
    KOSDAQ_MID = ['021320', '046440', '215000', '215200', '206560']
    # 021320 [KCC건설: 건설], 046440 [KG모빌리언스: IT / SW], 215000 [골프존: IT / SW], 215200 [메가스터디교육: 기타/서비스], 206560 [덱스터 : 오락 문화]
    KOSDAQ_SML = ['060310', '052220', '036120', '032540', '078130']
    #  060310 [3S : 제조], 052220 [iMBC : IT/SW], 036120 [SCI평가정보 : 기타서비스], 032540 [TJ미디어 : 제조], 078130 [국일제지 : 제조]

    # 기술적 분석 크롤링
    get_kosdaq_technical_info(code_list=KOSDAQ_MID, str_datefrom="2018-01-01")





    # Load 기술, 기본 분석 데이터
    # df = load_data(code_list=["035420"], save_date="2019-11-07")
    # print (df)