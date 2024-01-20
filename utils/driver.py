from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
def find_text(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)


    wait = WebDriverWait(driver, 20)
    print(driver.title)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    text=driver.title+""

    h1 = soup.find("h1")
    if h1 :
        h1=h1.text
        text=text+h1+","
      
    h2 = soup.find("h2")
    if h2 :
        h2=h2.text
        text=text+h2+","
    
    h3 = soup.find("h3")
    if h3 :
        h3=h3.text
        text=text+h3+","
        
    strong = soup.find("strong")
    if strong :
        strong=strong.text
        text=text+strong
    print(text)
    driver.quit()
    return text
