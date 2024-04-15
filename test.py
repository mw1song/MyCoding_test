from selenium import webdriver
from bs4 import BeautifulSoup

# 크롬 드라이버 경로 설정
chrome_driver_path = "크롬 드라이버의 경로를 여기에 입력하세요"

# 크롬 브라우저 열기
driver = webdriver.Chrome()

# 웹페이지 열기
url = "https://www.google.com/search?newwindow=1&sca_esv=59018620b3723b92&sxsrf=ACQVn0_7Ysv8UK1lb1uB99jDlyguWMgcNg:1712990014188&q=aws+telco+RAN&tbm=nws&source=lnms&prmd=isnvbmz&sa=X&ved=2ahUKEwi_rLKKyb6FAxX9i68BHUO0BmgQ0pQJegQIChAB"
driver.get(url)


# 페이지 소스 가져오기
page_source = driver.page_source

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 클래스를 사용하여 링크 가져오기
links = soup.find_all(class_='WlydOe')

# 각 링크의 href 속성을 출력
for link in links:
    href = link.get('href')
    print(href)
