import data_processor
import logging
import os
import sys

from common import util
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
    # data_processor.get_stock_technical_info(code_list=KOSPI, str_datefrom="2018-01-01", save_date="2019-11-07") # 네이버는 수정주가가 아님... 손절
    data_processor.get_stock_technical_info(code_list=KOSPI, num_days=1000, save_date="2019-11-17")
    # 기본적 분석 크롤링
    data_processor.get_stock_fundamental_info(code_list=KOSPI, save_date="2019-11-17")

    ###########################################
    # Load 기술, 기본 분석 데이터
    ###########################################
    df = data_processor.load_data(code_list=KOSPI, save_date="2019-11-17")

    for stock_code in ["035420"]:
        log_dir = os.path.join(util.BASE_DIR, 'logs/%s' % stock_code)
        timestr = util.timestr
        if not os.path.exists('logs/%s' % stock_code):
            os.makedirs('logs/%s' % stock_code)
        file_handler = logging.FileHandler(filename=os.path.join(log_dir, "%s_%s.log" % (stock_code, timestr)), encoding='utf-8')
        stream_handler = logging.StreamHandler(sys.stdout)
        file_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.INFO)
        logging.basicConfig(format="%(message)s", handlers=[file_handler, stream_handler], level=logging.DEBUG)

        code_data = df[df['code'] == stock_code]
        prep_data = data_processor.preprocess(code_data)
        training_data = data_processor.build_training_data(prep_data)

        # 기간 필터링
        testing_data = training_data[(training_data['date'] >= '2019-01-01') & (training_data['date'] <= '2019-12-31')]
        training_data = training_data[(training_data['date'] >= '2016-01-01') & (training_data['date'] <= '2018-12-31')]
        # training_data = training_data.dropna()

        # 차트 데이터 분리
        features_chart_data = ['date', 'open', 'high', 'low', 'close', 'volume']
        chart_data = training_data[features_chart_data]

        # 학습 데이터 분리
        features_training_data = [
            'open_lastclose_ratio', 'high_close_ratio', 'low_close_ratio',
            'close_lastclose_ratio', 'volume_lastvolume_ratio',
            'close_ma5_ratio', 'volume_ma5_ratio',
            'close_ma10_ratio', 'volume_ma10_ratio',
            'close_ma20_ratio', 'volume_ma20_ratio',
            'close_ma60_ratio', 'volume_ma60_ratio',
            'close_ma120_ratio', 'volume_ma120_ratio'
        ]
        training_data = training_data[features_training_data]
        training_data = training_data.dropna()

        # # 강화학습 시작
        policy_learner = PolicyLearner(stock_code=stock_code, chart_data=chart_data, training_data=training_data, min_trading_unit=1, max_trading_unit=5, delayed_reward_threshold=.05, lr=.01)
        policy_learner.fit(balance=10000000, num_epoches=500, discount_factor=0, start_epsilon=.25)

        # 정책 신경망을 파일로 저장
        model_dir = os.path.join(util.BASE_DIR, 'models/%s' % stock_code)
        if not os.path.isdir(model_dir):
            os.makedirs(model_dir)
        model_path = os.path.join(model_dir, 'model_%s.h5' % timestr)
        policy_learner.policy_network.save_model(model_path)

        # 학습한 모델로 투자 시뮬레이션
        model_ver = timestr
        chart_data = testing_data[features_chart_data]
        testing_data = testing_data[features_training_data]
        policy_learner = PolicyLearner(stock_code=stock_code, chart_data=chart_data, training_data=testing_data, min_trading_unit=1, max_trading_unit=5)
        policy_learner.trade(balance=10000000, model_path=os.path.join(util.BASE_DIR, 'models/{}/model_{}.h5'.format(stock_code, model_ver)))