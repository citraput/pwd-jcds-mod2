#Latihan:

# 1) Gunakan API Zomato
# - Cari Nama Resto
# Masukkan nama kota: 
# Output: Nama restaurant di kota tersebut

# - Cari Nama Resto
# Masukkan nama kota: 
# Output: Nama restaurant di kota tersebut
# Nama Resto : 
# 1. Jenis Resto (Establishment_Name)
# 2. Cuisine Name
# 3. Alamat
# 4. Rating (Angka)
# 5. No Telepon

# - Menu (Daily Menu)
# Masukkan Nama Resto: 
# Output: Menu yang tersedia di Resto Tersebut 

import requests
import json
import config

apiKey = config.apiKey
base_zomato_url = 'https://developers.zomato.com/api/v2.1/'
headInfo = {
        "user-key": apiKey
    }

#####################################################################
##### RESTAURANT SUGGESTION 
#####################################################################
def getCityID(cityname, apiKey, baseurl, headInfo):
    try:
        category = 'cities'
        
        if not cityname.replace(" ", "").isalpha():
            raise Exception("Invalid City.")

        cityname_split = cityname.split(" ")
        cityname_20 = "%20".join(cityname_split)
        
        data = requests.get(f'{base_zomato_url}{category}?q={cityname_20}', headers=headInfo)
        data = data.json()
        location_suggestions = data["location_suggestions"]
        
        if len(data['location_suggestions']) == 0:
            raise Exception()
        elif len(data['location_suggestions']) == 1:
            return (data['location_suggestions'][0]['id'], cityname)
        else:
            print("Do you mean: ")
            cities_and_id = []
            for city_suggestion in location_suggestions:
                cities_and_id.append({'name': city_suggestion['name'], 'id': city_suggestion['id']})

            cities = []
            cities_id = []
            count = 0
            for city in cities_and_id:
                count += 1
                cities.append(city["name"])
                cities_id.append(city["id"])
                print(f'{count}) {city["name"]}')
            try:
                choose_city = int(input("Please choose the number of your city? "))
                city_id = cities_id[choose_city - 1]
                city_name = cities[choose_city - 1]
                return (city_id, city_name)
            except:
                return 'The city is not available.'
    except:
        print("Data is not available.")

# Maksimal restaurant yang muncul 20
def getRestaurantByCity(cityname, apiKey, base_url, headInfo):
    try:
        category = 'search'
        cat_type = 'city'

        city_id, city_name = getCityID(cityname, apiKey, base_url, headInfo)
        cityname = cityname.replace(" ", "")
        # url = 'https://developers.zomato.com/api/v2.1/search?entity_id=11052&entity_type=city'
        url = f'{base_url}{category}?entity_id={city_id}&entity_type={cat_type}'
        data = requests.get(url, headers=headInfo)
        # print(data.status_code)
        data = data.json()
        restaurants = data["restaurants"]

        restos = []
        for restaurant in restaurants:
            temp = {}
            temp['name'] = restaurant["restaurant"]["name"]
            temp['jenis'] = restaurant["restaurant"]["establishment"]
            temp['cuisine'] = restaurant["restaurant"]["cuisines"]
            temp['alamat'] = restaurant["restaurant"]['location']['address']
            temp['rating_angka'] = float(restaurant["restaurant"]['user_rating']['aggregate_rating'])
            temp['no_telepon'] = restaurant["restaurant"]['phone_numbers']
            restos.append(temp)

        print("\n" + "-" * 50)
        print(f"** 20 Recommended Restaurants in {city_name} **")
        print("-" * 50)

        count = 0
        for i in restos:
            count += 1
            jenis = ''.join(i["jenis"])
            print(f'{count}) {i["name"]}\
                \n\tEstablishment: {jenis}\
                \n\tCuisine: {i["cuisine"]}\
                \n\tAddress: {i["alamat"]}\
                \n\tRating: {i["rating_angka"]}\
                \n\tPhone: {i["no_telepon"]}\n')

        with open(f'restaurantsin{cityname}.json', 'w') as file:
            json.dump(restos, file, indent=4)
        print(f'\nThe total of suggested restaurants in {cityname} is {len(restaurants)}.\n\
            ** The data of restaurants has been saved in "restaurantin{cityname}.json" file.')
    except:
        print('Invalid City.')

#####################################################################   
### RESTAURANT DAILY MENU
### Hanya Bisa diakses di Prague
### Pilih location: Prague
#####################################################################
def getRestaurantID(query, city, apiKey, base_url, headInfo):
    try:
        category = 'search'
        cat_type = 'city'

        city_id, cityname = getCityID(city, apiKey, base_url, headInfo)
        cityname = cityname.replace(" ", "")

        url = f'{base_url}{category}?entity_id={city_id}&entity_type={cat_type}&q={query}'
        data = requests.get(url, headers=headInfo)

        if data.status_code == 200:
            data = data.json()
            restaurants = data["restaurants"]

            if len(restaurants) == 0:
                raise Exception("Your restaurant name is not available.")
            else:
                restos = []
                for restaurant in restaurants:
                    restos.append({"res_name": restaurant["restaurant"]["name"], \
                            "res_id": restaurant["restaurant"]["id"], \
                            "alamat": restaurant["restaurant"]["location"]["address"]})
                print('\n\t' + '-'*50)
                print("\t** Do you mean: **")
                print('\t' + '-'*50)
                restos_name = []
                restos_id = []
                count = 0
                for i in restos:
                    count += 1
                    print(f'\t{count}) {i["res_name"]}, location: {i["alamat"]}')
                    restos_name.append(i['res_name'])
                    restos_id.append(i['res_id'])

                try:
                    choose_resto = int(input("Please input the number of your Restaurant: "))
                    res_id = restos_id[choose_resto - 1]
                    return res_id
                except:
                    return "Your restaurant name is not available"
        else:
            raise Exception()
    except:
        print("Invalid Restaurant Name.")

def getMenuByRestaurantID(query, city, apiKey, base_url, headInfo):
    try:
        category = 'dailymenu'
        res_id = getRestaurantID(query, city, apiKey, base_url, headInfo)

        url = f'{base_url}{category}?res_id={res_id}'
        data = requests.get(url, headers=headInfo)

        if data.status_code == 200:
            data = data.json()
            daily_menus = data["daily_menus"]
            print('\n\t' + '-'*50)
            print("\t** Daily Menus Available ** ")
            print('\t' + '-'*50)
            count = 0
            if len(daily_menus) == 0:
                print("\tNo Menu")
            else:
                for i in daily_menus:
                    for j in i["daily_menu"]["dishes"]:
                        count += 1
                        print(f'\t{count}) {j["dish"]["name"]}')
        elif data.status_code == 400:
            print(data.json()["message"])
        else:
            print("Invalid")
    except:
        print("No daily menu available.")
    
# https://developers.zomato.com/api/v2.1/dailymenu?res_id=16505937 --> succes
# 16507624 ==> success
# 16507625
# 19279193
# Monolok
# 16505937

def findRestaurantByCity(apiKey, base_zomato_url, headInfo):
    city = input("Please input city to find the best restaurant in your area? ")
    # print(getCityID(city, apiKey, base_zomato_url, headInfo))
    if city.replace(" ", "").isalpha() or ',' in city:
        getRestaurantByCity(city, apiKey, base_zomato_url, headInfo)
    else:
        print("Nama kota yang Anda masukkan salah.")

#####################################################################
## FIND RESTAURANT BY CITY
## function: findRestaurantByCity(apiKey, base_zomato_url, headInfo)
######################################################################

findRestaurantByCity(apiKey, base_zomato_url, headInfo)

def findMenuByRestoCity(apiKey, base_zomato_url, headInfo):
    resto = input("Please input the name of a restaurant: ")
    city = input("Please input the city location of the restaurant: ")
    # print(getRestaurantID(resto, city, apiKey, base_zomato_url, headInfo))
    getMenuByRestaurantID(resto, city, apiKey, base_zomato_url, headInfo)

######################################################################
## FIND DAILY MENU BY RESTAURANT AND CITY
## function: findMenuByRestoCity(apiKey, base_zomato_url, headInfo)
######################################################################

findMenuByRestoCity(apiKey, base_zomato_url, headInfo)