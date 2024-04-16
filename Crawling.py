# Import Selenium web driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# page loading wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome web driver path
# driver_path = "D:\Mycoding\chromedriver.exe"

# Open Chrome browser
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)  
driver.get("https://finance.yahoo.com")
driver.implicitly_wait(30)

wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yfin-usr-qry"]')))  # wait
elem = driver.find_element("xpath", "//*[@id='yfin-usr-qry']")  
elem.send_keys("AMZN")   # input company_ticker
elem.send_keys(Keys.RETURN)  # Enter 
# driver.implicitly_wait(30)   # wait

# find company name text
element = driver.find_element("xpath", '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
company_name = element.text

#Market_cap
element = driver.find_element("xpath", '//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]')  
Market_cap = element.text

# find HQ_Homepage
driver.find_element("xpath", '//*[@id="quote-nav"]/ul/li[6]/a/span').click()  
# driver.implicitly_wait(30)   # wait
# wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[1]')))  # wait
element = driver.find_element("xpath", '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[1]')  
HQ_Homepage = element.text.replace("\n", " ")

# Employees (Full Time Employees)
element = driver.find_element("xpath", '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[6]/span')  
Employees = element.text

# Key_members
element= driver.find_element("xpath", '//*[@id="Col1-0-Profile-Proxy"]/section/section[1]') 
# 텍스트를 줄 단위로 분할하여 리스트로 변환
Executives_lines = element.text.split('\n')

# Company_description
element= driver.find_element("xpath", '//*[@id="Col1-0-Profile-Proxy"]/section/section[2]/p')  
Company_description_eng = element.text

# from googletrans import Translator
# english_text = Company_description # 영문 텍스트
# translator = Translator()   # 번역기 생성
# Company_description_korean_text = translator.translate(english_text, dest='ko').text   # 영어에서 한국어로 번역
# # print(korean_text)   # 결과 출력


# Foundation_year
import re
match = re.search(r'(incorporated|founded)\s+in\s+(\d{4})\b', Company_description_eng, re.IGNORECASE)
if match:
    Foundation_year = match.group(2)
    # print("회사의 설립년도는", founding_year, "년입니다.")
else:
    print("설립년도를 찾을 수 없습니다.")

# Go to financials page
driver.find_element("xpath", '//*[@id="quote-nav"]/ul/li[7]/a/span').click()  
# driver.implicitly_wait(30)   # wait
driver.find_element("xpath", '//*[@id="Col1-1-Financials-Proxy"]/section/div[1]/div[2]/div/span').click()  # Annual confirm
# driver.implicitly_wait(30)   # wait

# Recent HQ_Homapagenue
element= driver.find_element("xpath", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[3]/span')  
Revenue = element.text
# Recent Net_income
element= driver.find_element("xpath", '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[19]/div[1]/div[3]/span')  
Net_income = element.text

# Recent 4 years HQ_Homapagenue
year_revenue = ''  # year_HQ_Homapagenue 변수를 빈 문자열로 초기화합니다.
for i in range(6, 2,-1):
    loc = '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[{}]/span'.format(i)
    element = driver.find_element("xpath", loc)
    year_revenue += element.text
    year_revenue += '\t'  # 탭 문자 추가
# print (year_HQ_Homapagenue)

# Recent 4 years Net_income
year_net_income = ''  # year_HQ_Homapagenue 변수를 빈 문자열로 초기화합니다.
for i in range(6,2,-1):
    loc = '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[19]/div[1]/div[{}]/span'.format(i)
    element = driver.find_element("xpath", loc)
    year_net_income += element.text
    year_net_income += '\t'  # 탭 문자 추가
# print (year_net_income)


# Go to Holders page
driver.find_element("xpath", '//*[@id="quote-nav"]/ul/li[10]/a/span').click()  
# driver.implicitly_wait(30)   # wait

# Key_holders_1 (Top Institutional Holders)
element= driver.find_element("xpath", '//*[@id="Col1-1-Holders-Proxy"]/section/div[2]/div[3]')  
# 텍스트를 줄 단위로 분할하여 리스트로 변환
lines = element.text.split('\n')
# 3번째부터 5번째 줄까지의 텍스트 추출
selected_line_text = '\n'.join(lines[0:5])
Key_holders_1 = selected_line_text

# Key_holders_2 (Top Mutual Fund Holders)
element= driver.find_element("xpath", '//*[@id="Col1-1-Holders-Proxy"]/section/div[2]/div[4]')  
# 텍스트를 줄 단위로 분할하여 리스트로 변환
lines = element.text.split('\n')
# 3번째부터 5번째 줄까지의 텍스트 추출
selected_line_text = '\n'.join(lines[0:5])
Key_holders_2 = selected_line_text



################################################################
######################## print all info ########################
################################################################
print("\n")
print("□ 회사명 : " + company_name,"('"+Foundation_year[2:4]+"年 설립)\n")

# HQ 위치만 발췌 
import re
only_HQ_location = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',HQ_Homepage)
HQ_location = only_HQ_location.strip()
print("□ 본사 : ", HQ_location,'\n')

# 홈페이지 URL 만 발췌 
urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', HQ_Homepage)
# 추출된 URL 출력
for url in urls:
    print("□ 홈페이지 : ", url, '\n')

print("□ 임원진")
for row in Executives_lines:
    if 'CEO' in row or 'CFO' in row or 'CTO' in row or 'Chairman' in row or 'President' in row or 'Chief Executive Officer' in row or 'Chief Technology Officer' in row or 'CTO' in row:
        print(row)
print('\n')
print("□ 임직원수 : " + Employees,"名\n")
print("□ 시가총액 : " + Market_cap + "$", "\n")  #수정필요
print("□ 경영현황 : 매출",Revenue +"K$ / ","손익", Net_income+"K$", "\n")
print("□ 주요주주 \n\n", Key_holders_1, "\n\n",Key_holders_2, "\n")
print("□ 회사개요 \n " + Company_description_eng, "\n") 
# print("□ 회사개요 \n " + Company_description_korean_text, "\n")  
# print("□ 주요사업분야 : " + Biz_area)

print("□ 사업현황")   # 년도별 매출 손익 출력

from datetime import datetime
# 현재 년도 가져오기
current_year = datetime.now().year
row_1="구분\t"
for year in range(current_year-4-2000, current_year-0-2000):
    row_1 += (str(year) + '年\t')  # 각 년도를 탭으로 구분하여 출력
print(row_1)
print("매출(K$)\t"+year_revenue)
print("손익(K$)\t"+year_net_income+'\n')

print("□ 최근동향")   # 최근 기사를 크롤링/출력
print("  - 기사제목 (날짜, 매체)")
print("     · (주요내용)")
print('\n')


# Keep the window floating until it is closed
while True:
    # 여기서 작업을 수행하거나 웹 페이지를 탐색할 수 있어요.
    # 예를 들어, 사용자 입력을 받아서 루프를 빠져나오는 조건을 만들 수 있어요.
    user_input = input("Press 'q' to quit: ")
    if user_input.lower() == 'q':
        break
# Exit web page
driver.quit()
