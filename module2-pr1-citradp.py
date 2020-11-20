from bs4 import BeautifulSoup
import requests
import json

url = 'http://www.scifijapan.com/articles/2015/10/04/bandai-ultraman-ultra-500-figure-list/'

web = requests.get(url)
data = BeautifulSoup(web.content, 'html.parser') 

strong = data.select('strong')
paragraph = data.select('div div div p')

# Menghilangkan <br/>
for e in data.findAll('br'):
    e.extract()

###############################
# VERSI 1
###############################
monsterhero = {
    "monster": [],
    "hero": []
}
jenis = ''

# .children: nama children tag html
#            harus pakai list untuk mengeluarkan isi per tag html
#            membuat list per setiap tag html
# .text: sudah jadi text, tidak memisahkan text per tag html
# .name: nama tagnya
for i in range(len(strong)):
    temp = list(strong[i].children)
    print(temp)
    if i > 0:
        # judul 'hero' atau 'monster' terdapat tag html 'span'
        # 'span' dapat diakses menggunakan .name
        if temp[0].name == 'span':
            if 'Monster' in temp[0].text:
                jenis = 'monster'
            else:
                jenis = 'hero'
            if 'Gashapon' in temp[0].text:
                element = temp
                # naik ke parent 'p' kemudian find_next_sibling 'p'
                element = list(strong[i].parent.find_next_sibling('p'))
                for i in element:
                    monsterhero[jenis].append(i)
        else:
            monsterhero[jenis].append(temp[0])

# print(monsterhero)

# membuat file monsterhero2.json
# 'w'; write monster hero dictionary to monsterhero2.json
# with open('monsterhero2.json', 'w') as file:
#     json.dump(monsterhero, file, indent=4)
# print(f'** Data berhasil disimpan di file {file.name}')


###############################
# # VERSI 2
###############################

karakter = {}
nomor = 1
no_keys = ''
for j in range(len(strong)):
    # 'Note' tidak dimasukkan, mulai dari index ke 1
    if j > 0:
        # Akses children (kasus disini: apapun di dalam tag p)
        temp = strong[j].children
        # print(list(temp))
        # Jika children indeks ke-1 dari p adalah tag span
        # Jika ada tag 'span' di temp
        if list(temp)[0].name == 'span':
            # print(f'{nomor}) {list(strong[j])[0].text}')
            nomor += 1
            # mengambil index ke 0, tidak mengambil bahasa jepang
            # mengambil judul/jenis ultraman
            no_keys = list(strong[j])[0].text
            # text dari span atau Jenis Hero/Monster akan menjadi key
            # di dictionary karakter
            karakter[no_keys] = []

            if 'Gashapon' in list(strong[j])[0].text:
                element = strong[j].parent.find_next_sibling('p')
                for el in list(element):
                    karakter[no_keys].append(el)
                #     print(el)
                # print(list(element))

        # Jika tidak ada children
        else:
            # print('\t' + str(strong[j].text))
            # Figure List dimasukan ke jenis masing-masing di dictionary 
            # karakter
            # memasukkan nama-nama ultraman tergantung jenis ultraman di no_key
            # ke dalam karakter[no_keys]
            karakter[no_keys].append(strong[j].text)

# json_mylist = json.dumps(karakter, separators=(',', ':'))
print(karakter)

print()
# with open('ultraman.json', 'w') as file:
#     json.dump(karakter, file, indent=4)
# print(f'** Data berhasil disimpan di file {file.name}')
