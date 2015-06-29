import requests, copy


def flipkart_offers():
    offers = []
    url = 'https://affiliate-api.flipkart.net/affiliate/offers/v1/dotd/json'
    headers = {
        'Fk-Affiliate-Id': 'shubhamgr1',
        'Fk-Affiliate-Token': 'd6935b0e76604db383d6421eda50a0ea'
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    offerData = data['dotdList']
    #offers.append(copy.deepcopy(offerData))
    offers += offerData

    url = 'https://affiliate-api.flipkart.net/affiliate/offers/v1/top/json'
    r = requests.get(url, headers=headers)
    data = r.json()

    offerData = data['topOffersList']
    #offers.append(copy.deepcopy(offerData))
    offers += offerData

    return offers


def flipkart_search(query):
    url = 'https://affiliate-api.flipkart.net/affiliate/search/json?query='+str(query)+'&resultCount=30'
    headers = {
        'Fk-Affiliate-Id': 'shubhamgr1',
        'Fk-Affiliate-Token': 'd6935b0e76604db383d6421eda50a0ea'
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    queryData = data['productInfoList']

    return queryData


if __name__=='__main__':
    flipkart_search('laptop')