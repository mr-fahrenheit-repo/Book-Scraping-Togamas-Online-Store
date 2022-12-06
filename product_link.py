# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import socket
import time
from path_source import chromedriver_path
from functions import progress_bar


# Configuring socket for scraping
socket.getaddrinfo('localhost', 8080)

def get_links(url, baseurl, scroll):
    # Product link (empty)
    productlinks = set()

    # Configuring selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent =Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246 ")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service = service, options= chrome_options)

    # Configuring webdriver render
    driver.set_window_size(1280,720)
    driver.get(url)
    # while True:
    #     try:
    #         time.sleep(5)
    #         driver.find_element(By.CLASS_NAME, "head_desc").text
    #         print("Loading page complete")
    #     except:
    #         continue
    #     else:
    #         break
     

    # Looping for scroll page
    for i in range(1,scroll):
        scrolling = (4160 * i)*i
        driver.execute_script(f"window.scrollTo(0, {scrolling})")
        time.sleep((2))
        # progress_bar(i + 1, scroll)
        
    # Getting product link
    base_url = baseurl
    content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(content, 'html.parser')
    lists = soup.find_all('div', class_= "produk_list")
    for y in lists:
        for a in y('a', href=True):
            link = base_url + a.get('href')
            productlinks.add(link)
    
    return productlinks