import data_processor
from policy_learner import PolicyLearner

if __name__ == "__main__":
    KOSPI = ["035420", "006800", "005930"]
    # 035420 NAVER, 006800 미래에셋대우, 005930 삼성전자
    KOSDAQ_MID = ['021320', '046440', '215000', '215200', '206560']
    # 021320 [KCC건설: 건설], 046440 [KG모빌리언스: IT / SW], 215000 [골프존: IT / SW], 215200 [메가스터디교육: 기타/서비스], 206560 [덱스터 : 오락 문화]
    KOSDAQ_SML = ['060310', '052220', '036120', '032540', '078130']
    #  060310 [3S : 제조], 052220 [iMBC : IT/SW], 036120 [SCI평가정보 : 기타서비스], 032540 [TJ미디어 : 제조], 078130 [국일제지 : 제조]

    ###########################################
    # get stock info
    ###########################################
    # 기술적 분석 크롤링
    data_processor.get_stock_technical_info(code_list=KOSPI, str_datefrom="2018-01-01", save_date="2019-11-07")
    # 기본적 분석 크롤링
    data_processor.get_stock_fundamental_info(code_list=KOSPI, save_date="2019-11-07")

    ###########################################
    # Load 기술, 기본 분석 데이터
    ###########################################
    df = data_processor.load_data(code_list=KOSPI, save_date="2019-11-07")

    for stock_code in KOSPI:
        code_data = df[df['code'] == stock_code]
        prep_data = data_processor.preprocess(code_data)
        training_data = data_processor.build_training_data(prep_data)

        # 기간 필터링
        training_data = training_data[(training_data['date'] >= '2017-01-01') & (training_data['date'] <= '2017-12-31')]
        training_data = training_data.dropna()

        # 차트 데이터 분리
        features_chart_data = ['date', '시가', '고가', '저가', '종가', '거래량']
        chart_data = training_data[features_chart_data]

        # 학습 데이터 분리
        features_training_data = [
            '시가_last종가_비율', '고가_종가_비율', '저가_종가_비율',
            '종가_last종가_비율', '거래량_last거래량_비율',
            '종가_ma5_비율', '거래량_ma5_비율',
            '종가_ma10_비율', '거래량_ma10_비율',
            '종가_ma20_비율', '거래량_ma20_비율',
            '종가_ma60_비율', '거래량_ma60_비율',
            '종가_ma120_비율', '거래량_ma120_비율'
        ]
        training_data = training_data[features_training_data]

        # 강화학습 시작
        policy_learner = PolicyLearner(stock_code=stock_code, chart_data=chart_data, training_data=training_data, min_trading_unit=1, max_trading_unit=2, delayed_reward_threshold=.2, lr=.001)
        policy_learner.fit(balance=10000000, num_epoches=1000, discount_factor=0, start_epsilon=.5)