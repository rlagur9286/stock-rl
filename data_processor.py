from common.util import get_stock_technical_info
from common.util import get_stock_fundamental_info

if __name__ == "__main__":
    # code = '035420'  # NAVER
    # code = '006800'  # 미래에셋대우
    # code = '005930'  # 삼성전자

    ###########################################
    # get stock info
    ###########################################
    # 기술적 분석 크롤링
    get_stock_technical_info(code_list=["035420", "006800", "005930"], str_datefrom="2018-01-01")
    # 기본적 분석 크롤링
    get_stock_fundamental_info(code_list=["035420", "006800", "005930"])