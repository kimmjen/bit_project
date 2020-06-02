from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote_plus

def crawler(company_code, maxpage):
    
    page = 1 
    df_result = []
    while page <= int(maxpage): 
    
        url = 'https://finance.naver.com/item/news_news.nhn?code=' + str(company_code) + '&page=' + str(page) 
        source_code = requests.get(url).text
        html = BeautifulSoup(source_code, "lxml")
     
        # 뉴스 제목 
        titles = html.select('.title')
        title_result=[]
        for title in titles: 
            title = title.get_text() 
            title = re.sub('\n','',title)
            title_result.append(title)
 
 
        # 뉴스 링크
        links = html.select('.title') 
 
        link_result =[]
        news = []
        for link in links: 
            add = 'https://finance.naver.com' + link.find('a')['href']
            link_result.append(add)
            news.append(add)
        
        # 컨텐츠
        content_result = []
        for i in news:
            try:
                res = requests.get(i)
                content = res.text
                soup = BeautifulSoup(content, 'html.parser')
                body = soup.find(id='news_read')
                contents = body.text.strip()
                content_result.append(contents)
            except AttributeError as e:
                print('내용없음')
                continue
        # 뉴스 날짜 
        dates = html.select('.date') 
        date_result = [date.get_text() for date in dates] 
 
 
        # 뉴스 매체     
        sources = html.select('.info')
        source_result = [source.get_text() for source in sources] 
 
 
        # 변수들 합쳐서 해당 디렉토리에 csv파일로 저장하기 
 
        result= {"날짜" : date_result, "언론사" : source_result, "기사제목" : title_result, "기사내용" : content_result, "링크" : link_result} 
        df_result = pd.DataFrame(result)
        print(df_result)
        print("다운 받고 있습니다------")
        df_result.to_csv('page' + str(page) + '.csv', mode='w', encoding='utf-8-sig')
        page += 1
     
            
 
         

def main():
    info_main = input("="*50+"\n"+"실시간 뉴스기사 다운받기."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    
    company_code = input("종목이나 이름이나 코드 입력 : ")

    url = 'https://finance.naver.com/item/news_news.nhn?code='+str(company_code)
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    mydata = driver.find_element_by_class_name('type5')
    mydata = driver.page_source

    html = BeautifulSoup(mydata, 'lxml')
    navi = html.find("table", class_="Nnavi")
    navi_last = navi.find("td", class_="pgRR")
    pag = navi_last.a.get('href').rsplit('&')[1]
    pg_last = pag.split('=')[1]
    pg_last = int(pg_last)
    print("총 " + str(pg_last) + " 개 확인")
    
    maxpage = input("총 페이지 수 : ")
    crawler(company_code, maxpage)

main() 