from product_link import get_links
from page_scraping import get_detail
import pandas as pd

# Assigning variable for get_links functions
baseurl = 'https://togamas.com/' # web adress in string value
url =  'https://togamas.com/koleksi-3' # web adress in string value
scroll = 15 # Number of scroll page in Int value

# Getting product links
productlinks = get_links(url, baseurl, scroll)
print('total product links :',len(productlinks))
print(productlinks)
# list for the product detail
# judul = []
# deskripsi = []
# harga_retail = []
# harga_diskon = []
# penerbit = []
# penulis = []
# bahasa = []
# ISBN = []
# cover = []
# halaman = []
# berat = []
# panjang = []
# lebar = []
# gudang_sleman = []
# gudang_jogja = []
# link_foto = []

# Getting product detail
# for x in productlinks:
#     y = get_detail(x)
#     judul.append(y.get("judul", "Undefined"))
#     deskripsi.append(y.get("deskripsi", "Undefined"))
#     harga_retail.append(y.get("harga retail", "Undefined"))
#     harga_diskon.append(y.get("harga diskon", "Undefined"))
#     penerbit.append(y.get("penerbit", "Undefined"))
#     penulis.append(y.get("penulis", "Undefined"))
#     bahasa.append(y.get("bahasa", "Undefined"))
#     ISBN.append(y.get("isbn", "Undefined"))
#     cover.append(y.get("cover", "Undefined"))
#     halaman.append(y.get("halaman", "Undefined"))
#     berat.append(y.get("berat", "Undefined"))
#     panjang.append(y.get("panjang", "Undefined"))
#     lebar.append(y.get("lebar", "Undefined"))
#     gudang_sleman.append(y.get("gudang sleman", "Undefined"))
#     gudang_jogja.append(y.get("gudang jogja", "Undefined"))
#     link_foto.append(y.get("link foto", "Undefined"))
#     print("Data added: ", len(judul))

# Convert list into dataframe
# df = pd.DataFrame(list(judul,
#                        deskripsi,
#                        harga_retail,
#                        harga_diskon,
#                        penerbit,
#                        penulis,
#                        bahasa,
#                        ISBN,
#                        cover,
#                        halaman,
#                        berat,
#                        panjang,
#                        lebar,
#                        gudang_sleman,
#                        gudang_jogja,
#                        link_foto), 
#                   columns = ['judul',
#                        'deskripsi',
#                        'harga_retail',
#                        'harga_diskon',
#                        'penerbit',
#                        'penulis',
#                        'bahasa',
#                        'ISBN',
#                        'cover',
#                        'halaman',
#                        'berat',
#                        'panjang',
#                        'lebar',
#                        'gudang sleman',
#                        'gudang jogja',
#                        'link foto'
#                        ]
#                   )

# Export dataframe to csv
# csv = df.to_excel(r'C:\Users\rifky\Documents\Github\Book Scraping Togamas Online Store\Buku Best Seller\buku best seller.xlxs')
