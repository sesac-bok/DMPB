def get_call_rate(page, file_path):

    """ 콜금리
    - 네이버 콜금리 데이터
    - 2022년 11월 기준 page 623: 콜금리 데이터 2005년~

    ---------------------------------------------------------------------------

    - 함수 get_call_rate(page, file_path) -> callrate.csv로 저장

                    - page : 콜금리 데이터 페이지
                    
                    - file_path : to_csv 저장 경로 e.g.) C:/Users/사용자/Desktop"""
    
    import requests
    import datetime
    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup

    call_url= "https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_CALL&page={}"

    call_list= []

    for i in range(1,page):
        call_list.append(BeautifulSoup(requests.get(call_url.format(i), 'html.parser').text,'lxml').find_all('td'))

    result_list= []

    for list in call_list:        
        for i in range(len(list)//4):
            result_list.append({
                'date': list[4*i].text.strip(),
                'RATE': float(list[4*i+1].text)
            })    
    pd_result2= pd.DataFrame(result_list)
    pd_result2.date= pd_result2.date.astype('datetime64')

    # 원하는 전체 date range
    idx2= pd.date_range(pd_result2.date.min(), pd_result2.date.max())
    idx2= pd.Series(idx2)

    # 없는 행에 Nan을 넣어 병합한 후 Nan값을 이전 값으로 메꾸기
    callrate= pd.concat([pd.DataFrame({'date': idx2[~idx2.isin(pd_result2.date)], 'RATE': np.nan}),pd_result2]).sort_values('date').reset_index(drop=True).ffill(axis=0)
    
    callrate = callrate.merge(callrate.assign(date = callrate.date+pd.Timedelta(days=31)), 
               on='date',
               how='left', suffixes=['', '_30days_ago'])
    callrate.dropna(inplace=True)

    # 한달 전 콜 금리 비교 값
    callrate['change'] = np.select(
        condlist=[(callrate.RATE > callrate.RATE_30days_ago), (callrate.RATE == callrate.RATE_30days_ago),], 
        choicelist=['up', 'same',],
        default='down'
    )

    callrate.to_csv(path_or_buf= file_path + '/callrate.csv' ,index=False)
    
    return callrate