import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import msvcrt

def continue_execution():
    print("키 입력을 기다리는 중입니다...")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print("키 입력이 감지되었습니다.")
            break

# 여기에 다음 코드를 작성하시면 됩니다.



def google_search():
    # 선택된 라디오 버튼 확인
    operator = operator_var.get()
    
    # 검색어 입력 확인
    search_terms = []
    for entry in entry_list:
        term = entry.get()
        if term.strip() != "":
            search_terms.append(term)
    
    if not search_terms:
        messagebox.showwarning("경고", "적어도 하나의 검색어를 입력하세요.")
        return
    
    # 검색어 조합
    if operator == "AND":
        query = " AND ".join(search_terms)
    else:
        query = " OR ".join(search_terms)
        
    print (query)
    continue_execution()
    print("프로그램을 계속합니다.")
    
    
    # 웹 드라이버 초기화 및 구글 검색 페이지 열기
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    
    # 검색어 입력 후 검색 실행
    search_box = driver.find_element("xpath",'//*[@id="APjFqb"]')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

def on_closing():
    if messagebox.askokcancel("종료", "정말로 종료하시겠습니까?"):
        window.destroy()

# 윈도우 생성
window = tk.Tk()
window.title("Google 검색")
window.geometry("400x300")

# 검색어 입력을 위한 Entry 위젯 생성
entry_list = []
for i in range(5):
    entry = tk.Entry(window, width=40)
    entry.grid(row=i, column=0, padx=10, pady=5)
    entry_list.append(entry)

# AND/OR 선택을 위한 라디오 버튼 생성
operator_var = tk.StringVar()
operator_var.set("AND")
and_radio = tk.Radiobutton(window, text="AND", variable=operator_var, value="AND")
and_radio.grid(row=5, column=0, padx=10, pady=5)
or_radio = tk.Radiobutton(window, text="OR", variable=operator_var, value="OR")
or_radio.grid(row=6, column=0, padx=10, pady=5)

# 검색 버튼 생성
search_button = tk.Button(window, text="검색", command=google_search)
search_button.grid(row=7, column=0, padx=10, pady=10)

# 윈도우 실행
window.mainloop()

# 윈도우 종료 설정
# window.protocol("WM_DELETE_WINDOW", on_closing)