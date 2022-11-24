# pdfTotxt 함수 만들기

def pdfTotxt(mypdf_directory,mytxt_directory):

    '''
    pdf 내 텍스트를 추출해서 txt파일로 저장하는 함수 :
    -------------------------------------------------

    - input:
        - mypdf_directory : str, pdf파일들이 저장된 경로
        - mytxt_directory : str, 변환된 txt파일 저장할 폴더경로
    - output : 원하는 경로에 변환된 txt파일 저장
    
    '''

    from urllib.request import urlretrieve
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.request import urlretrieve
    import re
    import glob
    import pdfplumber

    #pdf파일들이 저장된 경로

    all_files = (glob.glob(mypdf_directory+"*.pdf"))

    #변환된 txt파일 내용담는 리스트
    bond_all_text=[]
    #변환된 txt파일 이름 리스트
    bond_txt_downloaded_files=[]

    #속도문제 발생시 파일 목록들을 나누어 진행 필요
    for file in all_files:
       
        file_name=file.split('/')[7] #pdf파일이름
        file_name=file.split('\\')[1]
        new_file_name = file_name.replace('.pdf', '.txt')#txt파일이름

        all_text=''
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages: #pdf파일별 전체 페이지 가져오기
                    #print(page)
                    string = page.extract_text().replace('\n', '') #줄바꿈제거
                    all_text = all_text + '\n' + string #전체페이지 합친 pdf별 전체텍스트
                
                #변환된 txt파일 저장
                with open(mytxt_directory+new_file_name, 'w',encoding='utf-8') as f:
                    f.write(all_text)
                    #print(string)

                bond_all_text.append(all_text) #pdf별로 빈리스트에 append

        except Exception as e:
            print(e)
        bond_txt_downloaded_files.append(new_file_name)

    #print(bond_all_text)
    print('변환된 txt 파일 수: ',len(bond_all_text))
    return bond_txt_downloaded_files