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

# Configuring socket for scraping
socket.getaddrinfo('localhost', 8080)

# Getting detail product from product links
def get_detail(url):
    # Configuring selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    service = Service(r'C:\Users\rifky\Documents\Github\Book Scraping Togamas Online Store\chromedriver.exe')
    driver = webdriver.Chrome(service = service, options= chrome_options)

    # Configuring webdriver render
    driver.set_window_size(1280,720)
    driver.get(url)
    time.sleep((19))

    # Looping for scroll page
    for i in range(1,3):
        scroll = 1500 * i
        driver.execute_script(f"window.scrollTo(0, {scroll})")
        time.sleep((1))
        driver.save_screenshot(f'{i}.png')
        print(f"loading : {i}")

    # Getting the page source
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Getting the product title
    judul = remove_unknown(soup.find('span', property="name").text)

    # Getting the product description
    deskripsi = remove_unknown(soup.find('span',itemprop="description").text)

    # Getting the product retail price
    hargaawal = number_plain(soup.find('div', class_="produk_hargaawal").text)

    # Getting the product base price
    harga = number_plain(soup.find('div', class_="produk_hargadiskon").text)

    # Getting the product image link
    link_buku = find_link(str(soup.find('meta', itemprop="image")))

    # Getting author of the product
    penulis = clean_text(soup.find('div', class_="head_penulis").text)

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
    penerbit = detail.get("Penerbit", "Undefined")

    # Getting year detail from product
    tahun =  detail.get("Tahun", "Undefined")

    # Getting pages detail from product
    halaman = detail.get("Halaman", "Undefined")

    # Getting weight detail from product 
    berat = detail.get("Berat", "Undefined")

    # Getting ISBN detail from product
    isbn = detail.get("ISBN/EAN", "Undefined")

    # Getting language detail from product
    bahasa = detail.get("Bahasa", "Indonesia")

    # Getting cover detail from product
    cover = detail.get("Cover", "Undefined")

    # Getting dimension detail from product
    dimensi = detail.get("Dimensi", "Undefined")
    if dimensi != "Undefined":
        list_dimensi = re.findall(r'\d+',dimensi)
        panjang = list_dimensi[0]
        lebar = list_dimensi[1]
    else:
        pass

    # Reconfiguring webdriver
    driver.set_window_size(1280,720)
    driver.get(url)

    # page scroll to load the javascript
    driver.execute_script(f"window.scrollTo(0, -500)")
    time.sleep(19)

    # Find and click the buy button
    driver.find_element(By.XPATH, '//*[@id="con_main"]/div[4]/div/div[2]/table[2]/tbody/tr/td[2]/button').click()
    time.sleep(19)

    # Getting the stok and warehouse information
    element = driver.find_element(By.NAME, 'kota').text
    if 'Sleman - Tersedia' in element:
        gudang_sleman = "tersedia"
    else:
        gudang_sleman = "kosong"
    if 'Yogyakarta - Tersedia' in element:
        gudang_jogja = "tersedia"
    else:
        gudang_jogja = "kosong"

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
        "gudang sleman" : gudang_sleman,
        "gudang jogja" : gudang_jogja,
        "link foto" : link_buku
    }
    
    return data