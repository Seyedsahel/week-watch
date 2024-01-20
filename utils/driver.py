from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://faradars.org/')


wait = WebDriverWait(driver, 20)
print(driver.title)
page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')
p_text=driver.title+""

h1 = soup.find("h1")
if h1 :
    h1=h1.text
    p_text=p_text+h1+","
    
    print(p_text)
h2 = soup.find("h2")
if h2 :
    h2=h2.text
    p_text=p_text+h2+","
   
    print(p_text)
h3 = soup.find("h3")
if h3 :
    h3=h3.text
    p_text=p_text+h3+","
    print(p_text)
strong = soup.find("strong")
if strong :
    strong=strong.text
    p_text=p_text+strong
print(p_text)
driver.quit()
