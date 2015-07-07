import requests, json
import copy

def foodpanda(lat=0, lng=0, id=0):
    headers = {
        'X-FP-API-KEY': 'android'
    }
    if id == 0:
        url = 'http://api.foodpanda.in/api/v4/areas/geocoding_reverse?latitude='+str(lat)+'&longitude='+str(lng)+'&limit=1'
        r = requests.get(url, headers=headers)
        data = r.json()['data']['items'][0]['main_area']['id']
        #print data
        url_new = 'http://api.foodpanda.in/api/v4/vendors?area_id=' + str(data)
        r = requests.get(url_new, headers=headers)
        data = r.json()['data']['items']
        return json.dumps(data)
    else:
        url_new = 'http://api.foodpanda.in/api/v4/vendors?area_id=' + str(id)
        r = requests.get(url_new, headers=headers)
        data = r.json()['data']
        restData = {}
        restData['restaurants'] = data['items']
        restData['area_id'] = str(id)
        return json.dumps(restData)

    return

if __name__ == '__main__':
    print foodpanda(lat=28.44, lng=77.42)
    print foodpanda(id=134144)