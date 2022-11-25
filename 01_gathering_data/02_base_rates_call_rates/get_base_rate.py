def get_base_rate(i, file_path):

    """ 기준금리 크롤링 함수

    - 한국은행 기준금리 추이
    - 2022년 11월 24일 기준: 1999년부터 2022년 11월 24일까지 54개의 기준금리

    -----------------------------------------------------

    - 함수 get_base_rate(i, file_path) -> baserate.csv로 저장

                    -i : 기준금리 데이터 갯수
                    
                    -file_path : to_csv 저장 경로 e.g.) C:/Users/사용자/Desktop """
    import requests
    import datetime
    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup            

    base_url= "https://www.bok.or.kr/portal/singl/baseRate/list.do?dataSeCd=01&menuNo=200643"
    response = requests.get(base_url, 'html.parser')
    soup= BeautifulSoup(response.text, 'lxml')

    dict_list= []
    # 1999년부터 2022년 11월까지 54개의 기준금리
    for i in range(i):
        dict_list.append({
            'date': pd.to_datetime(datetime.datetime.strptime(soup.find_all('td')[3*i].text + soup.find_all('td')[3*i+1].text, '%Y%m월 %d일')),
            'RATE': float(soup.find_all('td')[3*i+2].text)
        })

    pd_result= pd.DataFrame(dict_list)

    # date range 일별 추가
    idx= pd.date_range(pd_result.date.min(), pd_result.date.max())
    idx= pd.Series(idx)

    # 없는 행에 Nan을 넣어 병합한 후 Nan값을 이전 값으로 메꾸기
    baserate= pd.concat([pd.DataFrame({'date': idx[~idx.isin(pd_result.date)], 'RATE': np.nan}),pd_result]).sort_values('date').reset_index(drop=True).ffill(axis=0)
    
    baserate = baserate.merge(baserate.assign(date = baserate.date+pd.Timedelta(days=31)), 
               on='date',
               how='left', suffixes=['', '_30days_ago'])

    baserate.dropna(inplace=True) # 빈값 제거
    
    # 한달 전 기준 금리 비교 값
    baserate['change'] = np.select(
        condlist=[(baserate.RATE > baserate.RATE_30days_ago), (baserate.RATE == baserate.RATE_30days_ago),], 
        choicelist=['up', 'same',],
        default='down'
    )
    

    baserate.to_csv(path_or_buf= file_path + '/baserate.csv' ,index=False)
    
    return baserate