# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import socket
import time

# Configuring socket for scraping
socket.getaddrinfo('localhost', 8080)

def get_links(url, baseurl, scroll):
    # Product link (empty)
    productlinks = []

    # Configuring selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    service = Service(r'C:\Users\rifky\Documents\Github\Book Scraping Togamas Online Store\chromedriver.exe')
    driver = webdriver.Chrome(service = service, options= chrome_options)

    # Configuring webdriver render
    driver.set_window_size(1280,720)
    driver.get(url)
    time.sleep((15))

    # Looping for scroll page
    for i in range(1,scroll):
        scrolling = 1500 * i
        driver.execute_script(f"window.scrollTo(0, {scrolling})")
        time.sleep((15))
        print(f"loading : {i}")
        driver.save_screenshot(fr'C:\Users\rifky\Documents\Github\Book Scraping Togamas Online Store\checking\{i}.png')
        
    # Getting product link
    base_url = baseurl
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    lists = soup.find_all('div', class_= "produk_list")
    for y in lists:
        for a in y('a', href=True):
            link = base_url + a.get('href')
            productlinks.append(link)
    
    return productlinks