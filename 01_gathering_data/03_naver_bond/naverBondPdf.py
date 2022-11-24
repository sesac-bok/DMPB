# 함수만들기
def naverBondPdf_download(pages, mydirectory):

    '''

    네이버 채권 리포트 pdf 다운로드 함수:
    --------------------------------------------
    
    - input : 
        - pages : 다운로드할 페이지수, range(원하는 페이지수)로 지정해주기 
        - mydirectory :str, 저장할 디렉토리(C:/Users/Choi/workspace/sesac/1117~ 기준금리예측플젝_/1.데이터수집/temp3/)
    - output : 원하는 경로에 pdf 파일이 저장 
    
    '''
    from urllib.request import urlretrieve
    from bs4 import BeautifulSoup
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.request import urlretrieve
    import re
    import datetime
    bond_base_url='https://finance.naver.com/research/debenture_list.naver?'

    #page지정해서 채권 리포트 pdf 다운로드받기

    for page in pages:
        

        page_url =bond_base_url+ "&page=" + str(page)
        page_req = urlopen(page_url)
        page_bs = BeautifulSoup(page_req, 'html.parser')
        #print(len(page_bs))

        #생성날짜, 증권사, 제목 가져오기
        bond_list=page_bs.select("div.box_type_m > table.type_1>tr")[1:]
        bond_pdf_downloaded_files=[]

        for bond in bond_list:
            bond_info_list=[]
            
            #print(bond)
            for bond_info in bond.select('td'):

                bond_info_list.append(bond_info)
            #print(bond_info_list)


            #print( bond_info_list)
            if len(bond_info_list)>1:
                title=bond_info_list[0].text #제목
                #print(title)
                company=bond_info_list[1].text #증권사이름
                #print(company)
                date=bond_info_list[3].text #생성날짜
                date = datetime.datetime.strptime(date, "%y.%m.%d").date()
                #print(date)
                #pdf download link   
                bond_pdf_download_href=bond_info_list[2].a.attrs['href']
                #print(bond_pdf_download_href)
                try:
                #pdf download link   
                    bond_pdf_download_href=bond_info_list[2].a.attrs['href']
                    #print(bond_pdf_download_href)
                    urlretrieve(bond_pdf_download_href, mydirectory + str(date) + "_" + company + "_"+title + ".pdf")
                except Exception as e:
                    print('error!', e)
                
                bond_pdf_downloaded_files.append(str(date) + "_" + company + "_"+title + ".pdf")
    print('저장된 pdf수 : ',len(bond_pdf_downloaded_files))

    return bond_pdf_downloaded_files
            
