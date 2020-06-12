from bs4 import BeautifulSoup
import requests
import json

url = 'http://www.scifijapan.com/articles/2015/10/04/bandai-ultraman-ultra-500-figure-list/'

web = requests.get(url)
data = BeautifulSoup(web.content, 'html.parser') 

strong = data.select('strong')
paragraph = data.select('div div div p')

for e in data.findAll('br'):
    e.extract()

# VERSI 1
monsterhero = {
    "monster": [],
    "hero": []
}

jenis = ''
for i in range(len(strong)):
    if i > 0:
        temp = strong[i].children
        if list(temp)[0].name == 'span':
            if 'Monster' in list(strong[i])[0].text:
                jenis = 'monster'
            else:
                jenis = 'hero'

            if 'Gashapon' in list(strong[i])[0].text:
                element = strong[i].parent.find_next_sibling('p')
                for el in list(element):
                    monsterhero[jenis].append(el)
                    print(el)
                print(list(element))
                
                # for el in element:
                #     print(el.text)
        else:
            monsterhero[jenis].append(strong[i].text)


# print(monsterhero)
print()
with open('monsterhero.json', 'w') as file:
    json.dump(monsterhero, file, indent=4)
print(f'** Data berhasil disimpan di file {file.name}')

# VERSI 2
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
            # print(f'{nomor}) {list(strong[j])[0].text}')
            nomor += 1
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
            karakter[no_keys].append(strong[j].text)

# json_mylist = json.dumps(karakter, separators=(',', ':'))
# print(karakter)

print()
with open('ultraman.json', 'w') as file:
    json.dump(karakter, file, indent=4)
print(f'** Data berhasil disimpan di file {file.name}')
