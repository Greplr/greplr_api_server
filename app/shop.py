import copy

import requests


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
    # offers.append(copy.deepcopy(offerData))
    offers += offerData

    url = 'https://affiliate-api.flipkart.net/affiliate/offers/v1/top/json'
    r = requests.get(url, headers=headers)
    data = r.json()

    offerData = data['topOffersList']
    # offers.append(copy.deepcopy(offerData))
    offers += offerData

    return offers


def flipkart_search(query):
    url = 'https://affiliate-api.flipkart.net/affiliate/search/json?query=' + str(query) + '&resultCount=30'
    headers = {
        'Fk-Affiliate-Id': 'shubhamgr1',
        'Fk-Affiliate-Token': 'd6935b0e76604db383d6421eda50a0ea'
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    filler_dict = {}
    final_list = []

    queryData = data['productInfoList']
    for x in queryData:
        # print x['productBaseInfo']
        # filler_dict['title'] = x['productBaseInfo']['productIdentifier']['categoryPaths']['categoryPath'][0]['title']
        filler_dict['title'] = x['productBaseInfo']['productIdentifier']['categoryPaths']['categoryPath'][0][0]['title']
        filler_dict['productId'] = x['productBaseInfo']['productIdentifier']['productId']
        for keys in x['productBaseInfo']['productAttributes']:
            if keys == 'imageUrls':
                filler_dict[keys] = {}
                # print x['productBaseInfo']['productAttributes'][keys]
                for i in x['productBaseInfo']['productAttributes'][keys]:
                    # print '_'+i, "++++++++++++=", keys
                    name = '_' + i
                    # print x['productBaseInfo']['productAttributes'][keys][i]
                    filler_dict[keys][name] = x['productBaseInfo']['productAttributes'][keys][i]
            else:
                filler_dict[keys] = x['productBaseInfo']['productAttributes'][keys]

        final_list.append(copy.deepcopy(filler_dict))
        # print final_list

    return final_list


if __name__ == '__main__':
    print flipkart_search('laptop')
