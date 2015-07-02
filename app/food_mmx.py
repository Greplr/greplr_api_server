import requests, copy, json

def food_mmx(lat, lng):

    #url = 'https://api.zomato.com/v1/search.json/near?lat=28.734371&lon=77.1197519&count=30'
    url = 'https://api.zomato.com/v1/search.json/near?lat='+str(lat)+'&lon='+str(lng)+'&count=30'
    headers = {
        'X-Zomato-API-Key': 'b0a3693c6ce448dca050334ee6acb945',
        'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; D5103 Build/18.1.A.2.25)'
    }

    r = requests.get(url, headers=headers)
    print r.headers, "+++++++++=================================="
    data = r.json()

    list_of_rest = data['results']
    #print sorted(list_of_rest, key=lambda x: x[u'result'][u'distance_actual'])
    #### Already sorted ####

    return json.dumps(list_of_rest)

if __name__ == '__main__':
    print food_mmx(28.734371, 77.1197519)