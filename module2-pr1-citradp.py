from bs4 import BeautifulSoup
import requests
import json

url = 'http://www.scifijapan.com/articles/2015/10/04/bandai-ultraman-ultra-500-figure-list/'

web = requests.get(url)
data = BeautifulSoup(web.content, 'html.parser') 

strong = data.select('strong')
karakter = {}
nomor = 1
no_keys = ''
for j in range(len(strong)):
    # 'Note' tidak dimasukkan, mulai dari index ke 1
    if j > 0:
        # Akses children di dalam tag p
        temp = strong[j].children
        # Jika children indeks ke-1 dari p adalah tag span
        if list(temp)[0].name == 'span':
            print(f'{nomor}) {list(strong[j])[0].text}')
            nomor += 1
            no_keys = list(strong[j])[0].text
            # text dari span atau Jenis Hero/Monster akan menjadi key
            # di dictionary karakter
            karakter[no_keys] = []
        # Jika tidak ada children
        else:
            print('\t' + str(strong[j].text))
            # Figure List dimasukan ke jenis masing-masing di dictionary 
            # karakter
            karakter[no_keys].append(strong[j].text)

# json_mylist = json.dumps(karakter, separators=(',', ':'))
# print(karakter)

with open('ultraman.json', 'w') as file:
    json.dump(karakter, file, indent=4)
print(f'Data berhasil disimpan di file {file.name}')
