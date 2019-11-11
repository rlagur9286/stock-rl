from common.util import get_stock_technical_info
from common.util import get_stock_fundamental_info
from common.util import load_data
from common.util import preprocess


if __name__ == "__main__":
    # code = '035420'  # NAVER
    # code = '006800'  # 미래에셋대우
    # code = '005930'  # 삼성전자
    code_list = ["035420", "006800", "005930"]

    ###########################################
    # get stock info
    ###########################################
    # 기술적 분석 크롤링
    get_stock_technical_info(code_list=code_list, str_datefrom="2018-01-01", save_date="2019-11-07")
    # 기본적 분석 크롤링
    get_stock_fundamental_info(code_list=code_list, save_date="2019-11-07")

    ###########################################
    # Load 기술, 기본 분석 데이터
    ###########################################
    df = load_data(code_list=code_list, save_date="2019-11-07")
    
    for code in code_list:
        code_data = df[df['code'] == code]
        prep_data = preprocess(code_data)
        print(prep_data)