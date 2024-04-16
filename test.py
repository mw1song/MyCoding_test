# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def News_sum():
    # Wait until the news articles are loaded
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.SoAPf')))

    # Get the HTML of the page
    html = driver.page_source
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Select all news articles
    articles = soup.select('.WlydOe')

    # Print the title, date, and source of each article
    for article in articles:
        title = article.select_one('.n0jPhd.ynAwRc.MBeuO.nDgy9d').text.strip()
        date = article.select_one('.OSrXXb.rbYSKb.LfVVr').text.strip()
        source = article.select_one('.MgUUmf.NUnG9d').text.strip()
        summary = article.select_one('.GI74Re.nDgy9d').text.strip()
        
        print("   - ",f"{title} ({date}, {source})")
        print("       · ",f"{summary}")


# Set up Selenium web driver
driver = webdriver.Chrome()
driver.get("https://www.google.com")

# Search for "AWS AND Telco"
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("AWS AND Telco")
search_box.send_keys(Keys.RETURN)

# Click on the "News" tab
news_tab = driver.find_element('xpath', '//*[@id="hdtb-sc"]/div/div/div[1]/div[3]/a/div')
news_tab.click()

# go to Next page
# Click on the page 2
news_init_page=2
news_last_page=5

# xpath_list = []

for i in range(news_init_page+1, news_last_page+1):
    xpath = '//*[@id="botstuff"]/div/div[3]/table/tbody/tr/td[{}]/a'.format(i)
    # xpath_list.append(xpath)
    news_tab = driver.find_element('xpath', xpath)
    news_tab.click()
    News_sum () 





# Keep the window floating until it is closed
while True:
    user_input = input("Press 'q' to quit: ")
    if user_input.lower() == 'q':
        break

# Exit web page
driver.quit()
