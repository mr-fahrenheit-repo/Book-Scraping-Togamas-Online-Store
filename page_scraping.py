# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import re
import socket
import time
from functions import find_link
from functions import remove_unknown
from functions import number_plain
from functions import clean_text
from path_source import chromedriver_path

# Configuring socket for scraping
socket.getaddrinfo('localhost', 8080)

# Getting detail product from product links
def get_detail(url):
    # Configuring selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent =Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246 ")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service = service, options= chrome_options)

    # Configuring webdriver render
    driver.set_window_size(1280,720)
    driver.get(url)
    print("Waiting the page to load...")
    while True:
        try:
            time.sleep(5)
            driver.find_element(By.CLASS_NAME, "head_desc").text
        except:
            continue
        else:
            break

    # Looping for scroll page
    for i in range(1,3):
        scroll = 1500 * i
        driver.execute_script(f"window.scrollTo(0, {scroll})")
        time.sleep((2))
        driver.execute_script(f"window.scrollTo(0, -{scroll})")
  
    print("Loading page complete")

    # Getting the page source
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Getting the product title
    try:
        judul = remove_unknown(soup.find('span', property="name").text)
    except:
        judul = "xxx"
    
    print("Judul added")

    # Getting the product description
    try:
        deskripsi = remove_unknown(soup.find('span',itemprop="description").text)
    except:
        deskripsi = "xxx"
        
    print("Deskripsi added")
    
    # Getting the product retail price
    try:
        hargaawal = number_plain(soup.find('div', class_="produk_hargaawal").text)
    except:
        hargaawal = "xxx"
    
    print("Harga retail added")
    
    # Getting the product base price
    try:
        harga = number_plain(soup.find('div', class_="produk_hargadiskon").text)
    except:
        harga = "xxx"
    
    print("Harga diskon added")
        
    # Getting the product image link
    try:
        link_buku = find_link(str(soup.find('meta', itemprop="image")))
    except:
        link_buku = "xxx"
    
    print("Link foto produk added")
        
    # Getting author of the product
    try:
        penulis = clean_text(soup.find('div', class_="head_penulis").text)
    except:
        penulis = "xxx"
    
    print("Penulis added")
        
    # Getting the product detail table information
    detail =  []       
    table = soup.find("div", { "class" : "list_table"})
    trs = table.find_all("tr")
    for tr in trs:
        tds = tr.find_all('td')
        for td in tds:
            detail.append(td.text) 
    detail = [x for x in detail if x != ":"]
    key = detail[::2]
    value = detail[1::2]
    detail = dict(zip(key, value))

    # Getting publisher detail from product
    try:
        penerbit = detail.get("Penerbit", "Undefined")
    except:
        penerbit = "xxx"
        
    print("Penerbit added")
        
    # Getting year detail from product
    try:
        tahun =  detail.get("Tahun", "Undefined")
    except:
        tahun = "xxx"
    
    print("Tahun added")
        
    # Getting pages detail from product
    try:
        halaman = detail.get("Halaman", "Undefined")
    except:
        halaman = "xxx"
    
    print("Halaman added")
        
    # Getting weight detail from product 
    try:
        berat = detail.get("Berat", "Undefined")
    except:
        berat = "xxx"
    
    print("Berat added")
        
    # Getting ISBN detail from product
    try:
        isbn = detail.get("ISBN/EAN", "Undefined")
    except:
        isbn = "xxx"
        
    print("ISBN added")
        
    # Getting language detail from product
    try:
        bahasa = detail.get("Bahasa", "Indonesia")
    except:
        bahasa = "xxx"
    
    print("Bahasa added")
        
    # Getting cover detail from product
    try:
        cover = detail.get("Cover", "Undefined")
    except:
        cover = "xxx"
    
    print("Cover added")
        
    # Getting dimension detail from product
    try:
        dimensi = detail.get("Dimensi", "Undefined")
        if dimensi != "Undefined":
            list_dimensi = re.findall(r'\d+',dimensi)
            panjang = list_dimensi[0]
            lebar = list_dimensi[1]
        else:
            pass
    except:
        panjang = "xxx"
        lebar = "xxx"
        
    print("Panjang added")
    print("Lebar added")
    
    # Shutting down the webdriver
    driver.quit()

    # Reopen webdriver
    driver.set_window_size(1280,720)
    driver.get(url)

    # page scroll to load the javascript
    driver.execute_script(f"window.scrollTo(0, -50000)")

    # Find and click the buy button    
    while True:
        try:
            time.sleep(10)
            driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[4]/div/div[2]/table[2]/tbody/tr/td[2]/button').click()
        except:
            continue
        else:
            break

    # Getting the stok and warehouse information
    print("Getting stok information")
    while True:
        try:
            time.sleep(5)
            element = driver.find_element(By.NAME, 'kota').text
        except:
            continue
        else:
            break
        
    if 'Sleman - Tersedia' in element:
        gudang_sleman = "tersedia"
    else:
        gudang_sleman = "kosong"
    if 'Yogyakarta - Tersedia' in element:
        gudang_jogja = "tersedia"
    else:
        gudang_jogja = "kosong"
        
    print("Stok gudang added")

    data = {
        "judul" : judul,
        "deskripsi" : deskripsi,
        "harga retail" : hargaawal,
        "harga diskon" : harga,
        "penerbit" : penerbit,
        "penulis" : penulis,
        "bahasa" : bahasa,
        "isbn" : isbn,
        "cover" : cover,
        "halaman" : halaman,
        "berat" : berat,
        "panjang" : panjang,
        "lebar" : lebar,
        "tahun" : tahun,
        "gudang sleman" : gudang_sleman,
        "gudang jogja" : gudang_jogja,
        "link foto" : link_buku
    }
    
    return data